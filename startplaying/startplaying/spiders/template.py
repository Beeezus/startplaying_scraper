from datetime import datetime, timezone


payload_template = {
    'operationName': 'UseGameSearchQuery',
    'variables': {
        'filter': {
            'costPerPlayer': {},
            'seatsLeft': {
                'gt': 0,
            },
            'public': True,
            'startTime': {
                'gte': f'{datetime.now(timezone.utc).isoformat()}',
            },
            'or': [
                {
                    'numPlayers': {
                        'gt': 0,
                    },
                },
                {
                    'startTime': {
                        'gte': f'{datetime.now(timezone.utc).isoformat()}',
                    },
                },
            ],
        },
        'limit': 30,
        'sort': {
            'key': 'startTime',
            'sortOrder': 'ASCENDING',
        },
        'search': None,
    },
    'query': 'query UseGameSearchQuery($after: Cursor, $filter: SessionFilter, $limit: Int, $sort: Sort!, $search: Search) {\n  sessions(\n    after: $after\n    limit: $limit\n    filter: $filter\n    sort: $sort\n    search: $search\n  ) {\n    edges {\n      node {\n        id\n        adventure {\n          id\n          costPerPlayer\n          created\n          earlyBirdDiscount\n          instantBook\n          maxPlayers\n          slug\n          title\n          __typename\n        }\n        event {\n          id\n          flagImage\n          title\n          __typename\n        }\n        gameTemplate {\n          id\n          coverImage\n          experienceLevel\n          gamePlatforms\n          gameSystems {\n            id\n            name\n            __typename\n          }\n          introduction\n          minDuration\n          maxDuration\n          __typename\n        }\n        host {\n          id\n          gmProfile {\n            gmStats {\n              numReviews\n              totalStarRating\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        numPlayers\n        slug\n        startTime\n        type\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n      __typename\n    }\n    __typename\n  }\n}',
}