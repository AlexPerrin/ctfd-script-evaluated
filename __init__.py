from flask import Blueprint

from CTFd.plugins.flags import FlagException, get_flag_class

from CTFd.models import Challenges, Flags, db 
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.plugins.migrations import upgrade


class ScriptChallenge(Challenges):
    __mapper_args__ = {"polymorphic_identity": "script"}
    id = db.Column(
        db.Integer, db.ForeignKey("challenges.id", ondelete="CASCADE"), primary_key=True
    )

    def __init__(self, *args, **kwargs):
        super(ScriptChallenge, self).__init__(**kwargs)
        self.value = kwargs["initial"]


class ScriptEvaluatedChallenge(BaseChallenge):
    id = "script"  # Unique identifier used to register challenges
    name = "script"  # Name of a challenge type
    templates = {  # Handlebars templates used for each aspect of challenge editing & viewing
        "create": "/plugins/script_evaluated/assets/create.html",
        "update": "/plugins/script_evaluated/assets/update.html",
        "view": "/plugins/script_evaluated/assets/view.html",
    }
    scripts = {  # Scripts that are loaded when a template is loaded
        "create": "/plugins/script_evaluated/assets/create.js",
        "update": "/plugins/script_evaluated/assets/update.js",
        "view": "/plugins/script_evaluated/assets/view.js",
    }
    # Route at which files are accessible. This must be registered using register_plugin_assets_directory()
    route = "/plugins/script_evaluated/assets/"
    # Blueprint used to access the static_folder directory.
    blueprint = Blueprint(
        "script",
        __name__,
        template_folder="templates",
        static_folder="assets",
    )
    challenge_model = ScriptChallenge

    @classmethod
    def evaluatorScript(cls, submission):
        evaluated = submission
        return evaluated

    @classmethod
    def attempt(cls, challenge, request):
        """
        This method is used to check whether a given input is right or wrong. It does not make any changes and should
        return a boolean for correctness and a string to be shown to the user. It is also in charge of parsing the
        user's input from the request itself.

        :param challenge: The Challenge object from the database
        :param request: The request the user submitted
        :return: (boolean, string)
        """
        data = request.form or request.get_json()
        submission = data["submission"].strip()
        submission = cls.evaluatorScript(submission)
        flags = Flags.query.filter_by(challenge_id=challenge.id).all()
        for flag in flags:
            try:
                if get_flag_class(flag.type).compare(flag, submission):
                    return True, "Correct"
            except FlagException as e:
                return False, str(e)
        return False, "Incorrect"


def load(app):
    upgrade(plugin_name="script_evaluated")
    CHALLENGE_CLASSES["script"] = ScriptEvaluatedChallenge
    register_plugin_assets_directory(
        app, base_path="/plugins/script_evaluated/assets/"
    )