from asok import Request, Form
from pygments import highlight
from pygments.lexers import HtmlLexer, PythonLexer
from pygments.formatters import HtmlFormatter


def make_form(request: Request) -> Form:
    """
    Creates and binds a native Asok Form with advanced input elements
    featuring customized CSS styling mappings.
    """
    return Form({
        'country': Form.dropdown(
            'Select Country', 
            ['Kinshasa', 'France', 'United States', 'United Kingdom', 'Germany', 'Japan', 'Canada', 'Australia'],
            searchable=True,
            rules='required',
            container__class='w-full relative',
            trigger__class='w-full flex items-center justify-between px-4 py-3 rounded-xl text-sm font-medium text-slate-200 bg-slate-800/80 border border-slate-700 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all cursor-pointer',
            menu__class='absolute top-full left-0 right-0 z-50 mt-2 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl overflow-hidden backdrop-blur-md',
            search__class='p-2 border-b border-slate-800',
            item__class='flex items-center px-4 py-3 text-sm text-slate-300 hover:bg-indigo-600 hover:text-white cursor-pointer transition-colors',
        ),
        'phone': Form.phone(
            'Phone Number', 
            default_country='CD', 
            rules='required',
            container__class='flex gap-2 w-full',
            select__class='px-3 py-3 rounded-xl text-sm font-medium text-slate-200 bg-slate-800/80 border border-slate-700 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all cursor-pointer max-w-[100px]',
            input__class='flex-1 px-4 py-3 rounded-xl text-sm font-medium text-slate-200 bg-slate-800/80 border border-slate-700 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 placeholder-slate-600 transition-all'
        ),
        'otp': Form.otp(
            'Verification Code (OTP)', 
            length=6, 
            rules='required|digits:6',
            container__class='flex gap-2 justify-between w-full max-w-[280px] mx-auto',
            input__class='w-10 h-10 text-center text-lg font-bold rounded-xl text-slate-200 bg-slate-800/80 border border-slate-700 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all'
        ),
        'toggle': Form.toggle(
            'Accept Terms', 
            rules='required',
            container__class='asok-toggle',
            slider__class='asok-toggle-slider'
        ),
        'rating': Form.rating(
            'Playground Rating', 
            max_stars=5, 
            rules='required',
            container__class='flex gap-1.5 items-center justify-center',
            star__class='text-amber-400 hover:scale-110 transition-transform cursor-pointer'
        ),
        'daterange': Form.daterange(
            'Booking Range', 
            start_label='Check-in', 
            end_label='Check-out', 
            rules='required',
            container__class='grid grid-cols-2 gap-4 w-full',
            field__class='flex flex-col gap-1.5',
            label__class='text-xs font-bold uppercase tracking-wider text-slate-400',
            input__class='w-full px-4 py-3 rounded-xl text-sm font-medium text-slate-200 bg-slate-800/80 border border-slate-700 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all'
        ),
    }, request)


def make_showcase_form(request: Request) -> Form:
    """
    Creates a showcase form schema containing all available native Asok field types.
    """
    return Form({
        'txt': Form.text('Text Input', placeholder='Type standard text...'),
        'email_fld': Form.email('Email Input', placeholder='you@example.com'),
        'pwd_fld': Form.password('Password Input', placeholder='••••••••'),
        'num_fld': Form.number('Number Input', placeholder='42'),
        'txtarea_fld': Form.textarea('Textarea Input', placeholder='Multi-line textarea...'),
        'checkbox_fld': Form.checkbox('Checkbox Control'),
        'select_fld': Form.select('Select Dropdown', [('a', 'Choice A'), ('b', 'Choice B')]),
        'radio_fld': Form.radio('Radio Group', [('yes', 'Yes'), ('no', 'No')]),
        'file_fld': Form.file('Single File Picker'),
        'date_fld': Form.date('Date Picker'),
        'time_fld': Form.time('Time Picker'),
        'datetime_fld': Form.datetime_local('Date-Time Picker'),
        'month_fld': Form.month('Month Picker'),
        'search_fld': Form.search('Search Box', placeholder='Search query...'),
        'url_fld': Form.url('URL Box', placeholder='https://example.com'),
        'tel_fld': Form.tel('Tel Box', placeholder='+1 (555) 0199'),
        'color_fld': Form.color('Color Picker'),
        'range_fld': Form.range('Range Slider', min='0', max='100', step='5'),
        'json_fld': Form.json('JSON Textarea', placeholder='{"key": "value"}'),
        'hdn_fld': Form.hidden(),
        
        # Advanced Widgets
        'dropdown_fld': Form.dropdown('Dropdown Selector', ['Kinshasa', 'Paris', 'New York']),
        'tags_fld': Form.tags('Tags Input', [('python', 'Python'), ('js', 'JavaScript'), ('rust', 'Rust')]),
        'daterange_fld': Form.daterange('Date Range Picker'),
        'timerange_fld': Form.timerange('Time Range Picker'),
        'toggle_fld': Form.toggle('Toggle Switch'),
        'otp_fld': Form.otp('OTP Input Boxes', length=6),
        'rating_fld': Form.rating('Rating Star Row'),
        'autocomplete_fld': Form.autocomplete('City Auto-complete', ['London', 'Los Angeles', 'Chicago']),
        'cascading_fld': Form.cascading('Cascading Option Selector', {
            'Europe': ['France', 'United Kingdom', 'Germany'],
            'Asia': ['Japan', 'China', 'India']
        }),
        'phone_fld': Form.phone('Int Phone Flags Picker', default_country='CD'),
        
        # Media & Rich Components
        'image_fld': Form.image('Image Live Preview', max_width=120, max_height=120),
        'files_fld': Form.files('Multi-file List', max_files=5),
        'wysiwyg_fld': Form.wysiwyg('WYSIWYG Rich Editor', height=100),
        'dropzone_fld': Form.dropzone('Drag & Drop Zone', max_files=5),
        'signature_fld': Form.signature('Signature Drawpad', width=280, height=120),
        'transfer_fld': Form.transfer('Transfer Dual-Box', ['Read Permission', 'Write Permission', 'Delete Permission']),
        'treeselect_fld': Form.treeselect('Tree Hierarchy Select', [
            {
                'id': 1, 'name': 'Engineering', 'children': [
                    {'id': 2, 'name': 'Frontend'},
                    {'id': 3, 'name': 'Backend'}
                ]
            },
            {
                'id': 4, 'name': 'Marketing'
            }
        ]),
    }, request)


def render(request: Request):
    """
    Renders the forms playground page with clean Form states.
    """
    showcase_form = make_showcase_form(request)
    demo_form = make_form(request)
    return render_page(request, showcase_form, demo_form)


def action_submit_demo(request: Request):
    """
    Handles live AJAX form submission and validation.
    """
    showcase_form = make_showcase_form(request)
    demo_form = make_form(request)
    success = False
    validated_data = None

    if demo_form.validate():
        # Enforce that the terms toggle must be strictly checked ON ('1')
        if demo_form.toggle.value == "1":
            success = True
            validated_data = demo_form.data
        else:
            demo_form.toggle._error = "You must accept the terms to submit."

    return render_page(request, showcase_form, demo_form, success=success, validated_data=validated_data)


def action_reset_demo(request: Request):
    """
    Resets the form fields and errors to their original defaults.
    """
    showcase_form = make_showcase_form(request).reset()
    demo_form = make_form(request).reset()
    return render_page(request, showcase_form, demo_form, success=False, validated_data=None)


def render_page(request: Request, showcase_form: Form, form: Form, success: bool = False, validated_data=None):
    """
    Helper function to render/stream page.asok with correct syntax highlights.
    """
    # 1. Python implementation snippet
    python_code = """# Python definition & validation
from asok import Request, Form

def make_form(request: Request) -> Form:
    return Form({
        'country': Form.dropdown(
            'Select Country', 
            ['Kinshasa', 'France', 'United States', 'United Kingdom', 'Germany', 'Japan', 'Canada', 'Australia'],
            searchable=True,
            rules='required'
        ),
        'phone': Form.phone(
            'Phone Number', 
            default_country='CD', 
            rules='required'
        ),
        'otp': Form.otp(
            'Verification Code (OTP)', 
            length=6, 
            rules='required|digits:6'
        ),
        'toggle': Form.toggle(
            'Accept terms', 
            rules='required'
        ),
        'rating': Form.rating(
            'Playground Rating', 
            max_stars=5, 
            rules='required'
        ),
        'daterange': Form.daterange(
            'Booking Range', 
            start_label='Check-in', 
            end_label='Check-out', 
            rules='required'
        ),
    }, request)

def render(request: Request):
    form = make_form(request)
    return request.stream("page.asok", form=form)

def action_submit_demo(request: Request):
    form = make_form(request)
    if form.validate():
        if form.toggle.value == "1":
            # Success! Access data: form.data
            return render_page(request, form, success=True, validated_data=form.data)
        else:
            form.toggle._error = "You must accept the terms and conditions."
    return render_page(request, form)
"""

    # 2. HTML template markup snippet
    html_code = """<!-- HTML Rendering with Tailwind CSS & custom styling -->
<form method="POST" data-action="submit_demo" data-block="form-demo-block" class="space-y-6">
    {{ request.csrf_input() }}
    
    <!-- Searchable Country Dropdown -->
    <div class="flex flex-col gap-1.5">
        <label class="text-xs font-bold uppercase tracking-wider text-slate-400">Country</label>
        {{ form.country.input(
            trigger__class="w-full flex items-center justify-between px-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-slate-200",
            menu__class="absolute top-full left-0 right-0 z-50 mt-2 bg-slate-900 border border-slate-700 rounded-xl overflow-hidden shadow-2xl",
            item__class="px-4 py-3 text-sm text-slate-300 hover:bg-indigo-600 hover:text-white cursor-pointer"
        ) }}
        {% if form.country._error %}
            <p class="text-xs text-rose-400">{{ form.country._error }}</p>
        {% endif %}
    </div>

    <!-- Phone Number Input -->
    <div class="flex flex-col gap-1.5">
        <label class="text-xs font-bold uppercase tracking-wider text-slate-400">Phone</label>
        {{ form.phone.input(
            select__class="px-3 py-3 rounded-xl bg-slate-800 border border-slate-700 text-slate-200",
            input__class="flex-1 px-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-slate-200"
        ) }}
        {% if form.phone._error %}
            <p class="text-xs text-rose-400">{{ form.phone._error }}</p>
        {% endif %}
    </div>

    <!-- OTP (One-Time Password) -->
    <div class="flex flex-col gap-1.5">
        <label class="text-xs font-bold uppercase tracking-wider text-slate-400">OTP Code</label>
        {{ form.otp.input(
            input__class="w-10 h-10 text-center rounded-xl bg-slate-800 border border-slate-700 text-slate-200"
        ) }}
        {% if form.otp._error %}
            <p class="text-xs text-rose-400">{{ form.otp._error }}</p>
        {% endif %}
    </div>

    <!-- Date Range Picker -->
    {{ form.daterange.input(
        input__class="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-slate-200"
    ) }}
    {% if form.daterange._error %}
        <p class="text-xs text-rose-400">{{ form.daterange._error }}</p>
    {% endif %}

    <button type="submit">Submit Form</button>
</form>"""

    formatter = HtmlFormatter(cssclass="codehilite", wrapcode=True)
    lexer_py = PythonLexer()
    lexer_html = HtmlLexer()

    showcase_codes = {
        'txt': {
            'py': "Form.text('Text Input', placeholder='Type standard text...')",
            'html': '{{ form.txt.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm") }}'
        },
        'email': {
            'py': "Form.email('Email Input', placeholder='you@example.com')",
            'html': '{{ form.email_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm") }}'
        },
        'pwd': {
            'py': "Form.password('Password Input', placeholder='••••••••')",
            'html': '{{ form.pwd_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm") }}'
        },
        'num': {
            'py': "Form.number('Number Input', placeholder='42')",
            'html': '{{ form.num_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm") }}'
        },
        'select': {
            'py': "Form.select('Select Dropdown', [('a', 'Choice A'), ('b', 'Choice B')])",
            'html': '{{ form.select_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm cursor-pointer") }}'
        },
        'radio': {
            'py': "Form.radio('Radio Group', [('yes', 'Yes'), ('no', 'No')])",
            'html': '{{ form.radio_fld.input(input__class="accent-indigo-600 mr-2 cursor-pointer w-4 h-4", label__class="inline-flex items-center text-sm text-slate-300 mr-6 cursor-pointer select-none") }}'
        },
        'checkbox': {
            'py': "Form.checkbox('Checkbox Control')",
            'html': '{{ form.checkbox_fld.input(class_="accent-indigo-600 w-4 h-4 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500/20 cursor-pointer mr-2.5") }}'
        },
        'date': {
            'py': "Form.date('Date Picker')",
            'html': '{{ form.date_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm") }}'
        },
        'time': {
            'py': "Form.time('Time Picker')",
            'html': '{{ form.time_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm") }}'
        },
        'datetime': {
            'py': "Form.datetime_local('Date-Time Picker')",
            'html': '{{ form.datetime_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm") }}'
        },
        'month': {
            'py': "Form.month('Month Picker')",
            'html': '{{ form.month_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm") }}'
        },
        'textarea': {
            'py': "Form.textarea('Textarea Input', placeholder='Multi-line textarea...')",
            'html': '{{ form.txtarea_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm min-h-[46px]") }}'
        },
        'search': {
            'py': "Form.search('Search Box', placeholder='Search query...')",
            'html': '{{ form.search_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm") }}'
        },
        'url': {
            'py': "Form.url('URL Box', placeholder='https://example.com')",
            'html': '{{ form.url_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm") }}'
        },
        'tel': {
            'py': "Form.tel('Tel Box', placeholder='+1 (555) 0199')",
            'html': '{{ form.tel_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm") }}'
        },
        'color': {
            'py': "Form.color('Color Picker')",
            'html': '{{ form.color_fld.input(class_="w-full h-[46px] p-1 rounded-xl bg-slate-800/60 border border-slate-700 cursor-pointer") }}'
        },
        'range': {
            'py': "Form.range('Range Slider', min='0', max='100', step='5')",
            'html': '{{ form.range_fld.input(class_="w-full accent-indigo-500 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer mt-3") }}'
        },
        'json': {
            'py': 'Form.json(\'JSON Textarea\', placeholder=\'{"key": "value"}\')',
            'html': '{{ form.json_fld.input(class_="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all text-sm font-mono min-h-[46px]") }}'
        },
        'file': {
            'py': "Form.file('Single File Picker')",
            'html': '{{ form.file_fld.input(class_="w-full text-xs text-slate-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 file:cursor-pointer transition-colors") }}'
        },
        'dropdown': {
            'py': "Form.dropdown('Dropdown Selector', ['Kinshasa', 'Paris', 'New York'])",
            'html': '{{ form.dropdown_fld.input(\n    trigger__class="w-full flex items-center justify-between px-4 py-3 rounded-xl text-sm font-medium text-slate-200 bg-slate-800/60 border border-slate-700 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all cursor-pointer",\n    menu__class="absolute top-full left-0 right-0 z-50 mt-2 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl overflow-hidden backdrop-blur-md",\n    item__class="px-4 py-3 text-sm text-slate-300 hover:bg-indigo-600 hover:text-white cursor-pointer transition-colors"\n) }}'
        },
        'tags': {
            'py': "Form.tags('Tags Input', [('python', 'Python'), ('js', 'JavaScript'), ('rust', 'Rust')])",
            'html': '{{ form.tags_fld.input(\n    container__class="relative",\n    selected__class="flex flex-wrap gap-1.5 p-2 bg-slate-800/60 border border-slate-700 rounded-xl min-h-[46px] items-center",\n    tag__class="inline-flex items-center gap-1 px-2.5 py-1 bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded-lg text-xs font-semibold",\n    add__class="text-xs font-bold text-indigo-400 hover:text-indigo-300 px-2 py-1 transition-colors cursor-pointer",\n    menu__class="absolute top-full left-0 right-0 z-[100] mt-2 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl overflow-hidden backdrop-blur-md max-h-48 overflow-y-auto",\n    option__class="flex px-4 py-3 text-sm text-slate-300 hover:bg-indigo-600 hover:text-white cursor-pointer transition-colors"\n) }}'
        },
        'daterange': {
            'py': "Form.daterange('Date Range Picker')",
            'html': '{{ form.daterange_fld.input(input__class="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 focus:outline-none focus:border-indigo-500 text-sm") }}'
        },
        'timerange': {
            'py': "Form.timerange('Time Range Picker')",
            'html': '{{ form.timerange_fld.input(input__class="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 focus:outline-none focus:border-indigo-500 text-sm") }}'
        },
        'rating': {
            'py': "Form.rating('Rating Star Row')",
            'html': '{{ form.rating_fld.input(container__class="flex gap-1", star__class="text-amber-400 hover:scale-110 transition-transform cursor-pointer") }}'
        },
        'toggle': {
            'py': "Form.toggle('Toggle Switch')",
            'html': '{{ form.toggle_fld.input }}'
        },
        'otp': {
            'py': "Form.otp('OTP Input Boxes', length=6)",
            'html': '{{ form.otp_fld.input(input__class="w-8 h-8 text-center text-md font-bold rounded-xl text-slate-200 bg-slate-800/60 border border-slate-700 focus:outline-none focus:border-indigo-500 transition-all") }}'
        },
        'autocomplete': {
            'py': "Form.autocomplete('City Auto-complete', ['London', 'Los Angeles', 'Chicago'])",
            'html': '{{ form.autocomplete_fld.input(\n    input__class="w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-200 focus:outline-none focus:border-indigo-500 text-sm",\n    menu__class="absolute top-full left-0 right-0 z-[60] mt-2 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl overflow-hidden backdrop-blur-md max-h-40 overflow-y-auto",\n    item__class="flex px-4 py-3 text-sm text-slate-300 hover:bg-indigo-600 hover:text-white cursor-pointer transition-colors"\n) }}'
        },
        'cascading': {
            'py': "Form.cascading('Cascading Option Selector', {'Europe': ['France', 'United Kingdom', 'Germany'], 'Asia': ['Japan', 'China', 'India']})",
            'html': '{{ form.cascading_fld.input(container__class="flex flex-col gap-2", select__class="w-full px-4 py-3 rounded-xl text-sm font-medium text-slate-200 bg-slate-800/60 border border-slate-700 focus:outline-none focus:border-indigo-500 cursor-pointer") }}'
        },
        'phone': {
            'py': "Form.phone('Int Phone Flags Picker', default_country='CD')",
            'html': '{{ form.phone_fld.input(select__class="px-3 py-3 rounded-xl text-sm font-medium text-slate-200 bg-slate-800/60 border border-slate-700 focus:outline-none focus:border-indigo-500 cursor-pointer max-w-[90px]", input__class="flex-1 px-4 py-3 rounded-xl text-sm font-medium text-slate-200 bg-slate-800/60 border border-slate-700 focus:outline-none focus:border-indigo-500") }}'
        },
        'transfer': {
            'py': "Form.transfer('Transfer Dual-Box', ['Read Permission', 'Write Permission', 'Delete Permission'])",
            'html': '{{ form.transfer_fld.input(\n    container__class="flex gap-4 items-center",\n    list__class="flex-1 flex flex-col gap-1 p-3 bg-slate-800/40 border border-slate-700 rounded-xl min-h-[160px] text-sm text-slate-300",\n    option__class="px-3 py-2",\n    button__class="p-2 px-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg transition-colors cursor-pointer",\n    actions__class="flex flex-col gap-2"\n) }}'
        },
        'treeselect': {
            'py': "Form.treeselect('Tree Hierarchy Select', [{'id': 1, 'name': 'Engineering', 'children': [...]}, ...])",
            'html': '{{ form.treeselect_fld.input(tree__class="border border-slate-700 rounded-xl p-4 bg-slate-800/40 max-h-48 overflow-y-auto text-sm text-slate-300", item__class="mb-2") }}'
        },
        'image': {
            'py': "Form.image('Image Live Preview', max_width=120, max_height=120)",
            'html': '{{ form.image_fld.input(input__class="w-full text-xs text-slate-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 file:cursor-pointer transition-colors", preview__class="rounded-xl border border-slate-700 object-cover mt-2 shadow-lg") }}'
        },
        'files': {
            'py': "Form.files('Multi-file List', max_files=5)",
            'html': '{{ form.files_fld.input(input__class="w-full text-xs text-slate-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 file:cursor-pointer transition-colors", item__class="inline-flex items-center gap-2 p-2 bg-slate-800/60 border border-slate-700 rounded-xl text-xs text-slate-300", img__class="w-8 h-8 rounded object-cover", btn__class="text-slate-400 hover:text-white font-bold px-1") }}'
        },
        'wysiwyg': {
            'py': "Form.wysiwyg('WYSIWYG Rich Editor', height=100)",
            'html': '{{ form.wysiwyg_fld.input(\n    container__class="flex flex-col border border-slate-700 rounded-xl overflow-hidden bg-slate-800/40",\n    toolbar__class="flex gap-2 p-2 border-b border-slate-700 bg-slate-900/50",\n    btn__class="p-1.5 px-3 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-bold text-slate-300 rounded transition-colors cursor-pointer",\n    editor__class="p-4 text-sm text-slate-200 focus:outline-none min-h-[120px] bg-slate-900/20"\n) }}'
        },
        'dropzone': {
            'py': "Form.dropzone('Drag & Drop Zone', max_files=5)",
            'html': '{{ form.dropzone_fld.input(\n    area__class="border-2 border-dashed border-slate-700 hover:border-indigo-500 bg-slate-800/20 rounded-xl p-8 text-center text-sm text-slate-400 cursor-pointer transition-colors",\n    input__class="hidden",\n    list__class="space-y-1.5",\n    item__class="flex items-center justify-between p-2.5 px-4 bg-slate-800/60 border border-slate-700 rounded-xl text-xs text-slate-300",\n    btn__class="text-rose-400 hover:text-rose-300 font-bold"\n) }}'
        },
        'signature': {
            'py': "Form.signature('Signature Drawpad', width=280, height=120)",
            'html': '{{ form.signature_fld.input(\n    container__class="w-full flex flex-col items-center gap-2",\n    canvas__class="border border-slate-700 rounded-xl bg-slate-950 shadow-inner",\n    btn__class="px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-bold text-slate-300 rounded-lg transition-colors cursor-pointer"\n) }}'
        }
    }

    codes = {}
    for key, val in showcase_codes.items():
        codes[key] = {
            'py': highlight(val['py'], lexer_py, formatter),
            'html': highlight(val['html'], lexer_html, formatter)
        }

    return request.stream("page.asok",
        showcase_form=showcase_form,
        form=form,
        success=success,
        validated_data=validated_data,
        codes=codes,
        python_html=highlight(python_code, lexer_py, formatter),
        html_html=highlight(html_code, lexer_html, formatter),
        seo_title="Interactive Forms Component - Asok Framework",
        description="Explore Asok's native form validation and advanced widgets including dropdowns, country phone code, OTP, rating, toggle and daterange."
    )
