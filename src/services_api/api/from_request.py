class FromRequest:
    def __init__(self, request):
        self.request = request

    def add_param(self, params, method):
        if method == 'GET':
            for key in params:
                my_request = self.request.GET.copy()
                my_request[key] = params[key]
                self.request.GET = my_request

    def get_data_key_number(self):
        result = {}
        for key in self.request.POST:
            if key.isdigit():
                on = self.request.POST.get(f'{key}-p')
                result[key] = {
                    'name': self.request.POST[key],
                    'on': True if on else False
                }
        return result

