# Troy swagger template
from drf_yasg import openapi


class ParamCollection(object):
    def __init__(self, name, model_name):
        self.name = name
        self.model_name = model_name

    def id_param(self):
        return openapi.Parameter(
            self.name,
            openapi.IN_PATH,
            description=str(self.model_name)+' PK',
            type=openapi.TYPE_INTEGER
        )


user_profile = ParamCollection(
    name='id',
    model_name='UserProfile'
)
trainee_profile = ParamCollection(
    name='id',
    model_name='TraineeProfile'
)
coach_profile = ParamCollection(
    name='id',
    model_name='CoachProfile'
)
