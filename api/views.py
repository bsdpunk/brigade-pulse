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
            COALESCE(100*((mg.members - four_weeks_ago.members)/four_weeks_ago.members), 100) as one_month_growth,
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
        ORDER BY growth_metric DESC
    """
    cursor = connection.cursor()
    cursor.execute(query)
    return JsonResponse(dictfetchall(cursor), safe=False)
