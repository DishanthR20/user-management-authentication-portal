from django.shortcuts import redirect

def user_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not request.session.get('user_id'):
            return redirect('login')

        response = view_func(request, *args, **kwargs)

        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response

    return wrapper

