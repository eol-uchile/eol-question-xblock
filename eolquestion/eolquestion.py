import json
import pkg_resources

from django.template import Context, Template

from webob import Response

from xblock.core import XBlock
from xblock.fields import Integer, String, Scope
from xblock.fragment import Fragment

# Make '_' a no-op so we can scrape strings
_ = lambda text: text


class EolQuestionXBlock(XBlock):

    display_name = String(
        display_name=_("Display Name"),
        help=_("Display name for this module"),
        default="Eol Question XBlock",
        scope=Scope.settings,
    )

    icon_class = String(
        default="other",
        scope=Scope.settings,
    )

    # TYPE
    type = String(
        display_name = _("Tipo"),
        help = _("Selecciona el tipo de pregunta"),
        default = "No Calificada",
        values = ["Calificada", "No Calificada", "Control"],
        scope = Scope.settings
    )

    # INDEX
    index = Integer(
        display_name = _("Indice"),
        help = _("Indica el indice de la pregunta"),
        default = 1,
        values = { "min" : 1, "step" : 1 },
        scope = Scope.settings
    )

    # TEXT
    text = String(
        display_name = _("Enunciado"),
        help = _("Indica el enunciado de la pregunta"),
        default = 'Enunciado ',
        values = { "minlength" : 5 },
        scope = Scope.settings
    )
    
    # THEME
    theme = String(
        display_name = _("Estilo"),
        help = _("Cambiar estilo de la pregunta"),
        default = "SumaySigue",
        values = ["SumaySigue", "Media", "Didactica"],
        scope = Scope.settings
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        context_html = self.get_context()
        template = self.render_template('static/html/eolquestion.html', context_html)
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/eolquestion.css"))
        frag.add_javascript(self.resource_string("static/js/src/eolquestion.js"))
        frag.initialize_js('EolQuestionXBlock')
        return frag

    def studio_view(self, context=None):
        context_html = self.get_context()
        template = self.render_template('static/html/studio.html', context_html)
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/eolquestion.css"))
        frag.add_javascript(self.resource_string("static/js/src/studio.js"))
        frag.initialize_js('EolQuestionStudioXBlock')
        return frag

    @XBlock.handler
    def studio_submit(self, request, suffix=''):
        self.display_name = request.params['display_name']
        self.type = request.params['type']
        self.index = request.params['index']
        self.text = request.params['text']
        self.theme = request.params['theme']
        return Response({'result': 'success'}, content_type='application/json')

    def get_context(self):
        return {
            'field_display_name': self.fields['display_name'],
            'field_type': self.fields['type'],
            'field_index': self.fields['index'],
            'field_text': self.fields['text'],
            'field_theme': self.fields['theme'],
            'xblock': self
        }
    
    def render_template(self, template_path, context):
        template_str = self.resource_string(template_path)
        template = Template(template_str)
        return template.render(Context(context))

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("EolQuestionXBlock",
             """<eolquestion/>
             """),
            ("Multiple EolQuestionXBlock",
             """<vertical_demo>
                <eolquestion
                theme='SumaySigue'
                type='Calificada'
                />
                <eolquestion
                theme='SumaySigue'
                type='No Calificada'
                />
                <eolquestion
                theme='SumaySigue'
                type='Control'
                />
                <eolquestion
                theme='Media'
                type='Calificada'
                />
                <eolquestion
                theme='Media'
                type='No Calificada'
                />
                <eolquestion
                theme='Media'
                type='Control'
                />
                <eolquestion
                theme='Didactica'
                type='Calificada'
                />
                <eolquestion
                theme='Didactica'
                type='No Calificada'
                />
                <eolquestion
                theme='Didactica'
                type='Control'
                />
                </vertical_demo>
             """),
        ]
