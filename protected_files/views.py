from django.http import HttpResponse, HttpResponseForbidden



def protected_file(request, file_path, redirect_root="", perm=None):
    """
    Checks permissions and returns an HttpResponse with the path to the file
    modified from http://www.djangosnippets.org/snippets/491/
    
    """
    if perm and request.user.has_perm(perm):
        response = HttpResponse()
        url = '%s/%s' % (redirect_root, file_path)
        
        # Nginx only
        # let nginx determine the correct content type 
        response['Content-Type']=""
        response['X-Accel-Redirect'] = url
        return response
    
    return HttpResponseForbidden()
