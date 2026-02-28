import yaml
from django import forms
from django.utils.safestring import mark_safe


class YAMLEditorWidget(forms.Textarea):
    def __init__(self, attrs=None):
        default_attrs = {
            "class": "yaml-editor",
            "rows": 20,
            "cols": 80,
            "style": "font-family: monospace;",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

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
        )

    def render(self, name, value, attrs=None, renderer=None):
        textarea = super().render(name, value, attrs, renderer)
        js_code = f"""
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            var textarea = document.querySelector('textarea[name="{name}"]');
            if (textarea) {{
                var editor = CodeMirror.fromTextArea(textarea, {{
                    mode: 'yaml',
                    theme: 'monokai',
                    lineNumbers: true,
                    indentUnit: 2,
                    tabSize: 2,
                    lineWrapping: true,
                    autoCloseBrackets: true,
                    matchBrackets: true,
                    lint: true
                }});

                // Auto-format on blur
                textarea.form.addEventListener('submit', function(e) {{
                    editor.save();
                }});
            }}
        }});
        </script>
        """
        return mark_safe(textarea + js_code)
