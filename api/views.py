from django.db import connection
from django.http import JsonResponse


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


def get_brigades_by_activity(request):
    query = """
        SELECT b.id,
            b.name,
            b.city,
            b.latitude,
            b.longitude,
            b.started_on,
            b.website,
            (SELECT COUNT(p.id) FROM project p WHERE p.brigade_id=b.id) as projects,
            mg.members as current_members,
            COALESCE(100*((mg.members - four_weeks_ago.members)/four_weeks_ago.members), 0) as one_month_growth,
            (COALESCE(100*((mg.members - four_weeks_ago.members)/four_weeks_ago.members), 0) +
            COALESCE(100*((mg.members - two_weeks_ago.members)/two_weeks_ago.members), 0) +
            COALESCE(100*((mg.members - one_week_ago.members)/one_week_ago.members), 0))/3 as growth_metric
        FROM brigade b
        LEFT JOIN
            (SELECT mg.brigade_id as brigade_id,
                avg(mts.members) as members
              FROM meetupgroup_time_series mts
              LEFT JOIN meetup_group mg ON mg.id = mts.original_model_id
              WHERE mts.timestamp >= current_date - interval '29 days'
                AND mts.timestamp <= current_date - interval '27 days'
              GROUP BY brigade_id
              ) as four_weeks_ago ON four_weeks_ago.brigade_id = b.id
        LEFT JOIN
            (SELECT mg.brigade_id as brigade_id,
                avg(mts.members) as members
              FROM meetupgroup_time_series mts
              LEFT JOIN meetup_group mg ON mg.id = mts.original_model_id
              WHERE mts.timestamp >= current_date - interval '15 days'
                AND mts.timestamp <= current_date - interval '13 days'
              GROUP BY brigade_id
              ) as two_weeks_ago ON two_weeks_ago.brigade_id = b.id
        LEFT JOIN
            (SELECT mg.brigade_id as brigade_id,
                avg(mts.members) as members
              FROM meetupgroup_time_series mts
              LEFT JOIN meetup_group mg ON mg.id = mts.original_model_id
              WHERE mts.timestamp >= current_date - interval '8 days'
                AND mts.timestamp <= current_date - interval '6 days'
              GROUP BY brigade_id
              ) as one_week_ago ON one_week_ago.brigade_id = b.id
        LEFT JOIN meetup_group mg ON mg.brigade_id = b.id
        WHERE b.type LIKE '%Brigade%' AND b.type LIKE '%Official'
        ORDER BY growth_metric DESC
    """
    cursor = connection.cursor()
    cursor.execute(query)
    return JsonResponse(dictfetchall(cursor), safe=False)


def get_brigade_profile(request, brigade_id):
    query = """
        SELECT b.id AS id,
          b.name AS brigade_name,
          b.city AS city,
          b.website AS website,
          mg.rating AS rating,
          mg.topics AS topics,
          mg.members AS members,
          (SELECT COUNT(p.id) FROM project p WHERE p.brigade_id=b.id) AS projects
        FROM brigade b
        LEFT JOIN meetup_group mg ON b.id = mg.brigade_id
        WHERE b.id='{}'
    """.format(brigade_id)
    cursor = connection.cursor()
    cursor.execute(query)
    d = dictfetchall(cursor)[0]

    query = """
        SELECT date_part('epoch',date_trunc('week', mts.timestamp))*1000 AS day, round(avg(mts.members)) AS members
              FROM meetupgroup_time_series mts
              LEFT JOIN meetup_group mg ON mg.id = mts.original_model_id
              WHERE mg.brigade_id='{}'
              GROUP BY date_trunc('week', mts.timestamp)
              ORDER BY date_trunc('week', mts.timestamp) ASC
    """.format(brigade_id)
    cursor.execute(query)
    d['meetup_members_time_series'] = dictfetchall(cursor)

    query = """
        SELECT date_part('epoch',date_trunc('week', grts.timestamp))*1000 AS day, count(grts.id) AS repos
              FROM githubrepository_time_series grts
              LEFT JOIN github_repository gr ON gr.id = grts.original_model_id
              LEFT JOIN project p ON p.github_repository_id = gr.id
              WHERE p.brigade_id='{}'
              GROUP BY date_trunc('week', grts.timestamp)
              ORDER BY date_trunc('week', grts.timestamp) ASC
    """.format(brigade_id)
    cursor.execute(query)
    d['repos_time_series'] = dictfetchall(cursor)

    query = """
        SELECT date_part('epoch',me.start_time)*1000 AS day, me.headcount AS headcount, me.name as name
              FROM meetup_event me
              WHERE me.brigade_id='{}' AND me.start_time < current_date AND me.headcount > 0
              ORDER BY me.start_time ASC
    """.format(brigade_id)
    cursor.execute(query)
    d['meetup_events_time_series'] = dictfetchall(cursor)

    return JsonResponse(d, safe=False)
