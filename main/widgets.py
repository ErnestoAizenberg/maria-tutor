from django import forms
from django.utils.safestring import mark_safe


class YAMLEditorWidget(forms.Textarea):
    """
    A widget that renders a YAML textarea enhanced with CodeMirror.
    """

    class Media:
        css = {
            "all": (
                "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/theme/monokai.min.css",
            )
        }
        js = (
            "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/yaml/yaml.min.js",
            "yaml_editor/js/yaml_editor.js",  # custom initialization script
        )

    def __init__(self, attrs=None, codemirror_options=None):
        """
        Initialize the widget.

        :param attrs: HTML attributes for the textarea.
        :param codemirror_options: Optional dict of CodeMirror options to override defaults.
        """
        default_attrs = {
            "class": "yaml-editor",
            "rows": 20,
            "cols": 80,
            "style": "font-family: monospace;",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

        # Store CodeMirror options for later use
        self.codemirror_options = codemirror_options or {}

    def get_codemirror_options(self):
        """
        Return the CodeMirror configuration options as a dictionary.
        Subclasses can override to change the default settings.
        """
        default_options = {
            "mode": "yaml",
            "theme": "monokai",
            "lineNumbers": True,
            "indentUnit": 2,
            "tabSize": 2,
            "lineWrapping": True,
            "autoCloseBrackets": True,
            "matchBrackets": True,
            "lint": True,
        }
        default_options.update(self.codemirror_options)
        return default_options

    def render(self, name: str, value, attrs=None, renderer=None):
        # Add a unique ID to the textarea if not already present, to make targeting easier
        if attrs is None:
            attrs = {}
        if "id" not in attrs:
            attrs["id"] = f"id_{name}"

        # Render the basic textarea
        textarea = super().render(name, value, attrs, renderer)

        # Pass the CodeMirror options as a data attribute on the textarea
        options = self.get_codemirror_options()
        options_json = mark_safe(str(options).replace("'", '"'))  # simple JSON-ish
        # Note: for production, use json.dumps()
        # In Django templates, you'd use json_script, but here we add a data attribute.
        # Instead of inline script, we rely on the external JS file which reads this attribute.
        script = f"""
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                var textarea = document.getElementById('{attrs["id"]}');
                if (textarea && window.CodeMirror) {{
                    // Initialize CodeMirror from the textarea
                    var editor = CodeMirror.fromTextArea(textarea, {options_json});
                    // Save editor content back to textarea on form submit
                    textarea.form.addEventListener('submit', function() {{
                        editor.save();
                    }});
                }}
            }});
        </script>
        """
        return mark_safe(textarea + script)
