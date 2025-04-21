from tauxs.models import Taux

class TauxMiddlware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        taux=Taux.objects.first()
        if taux is not None:
            request.session['taux_euro'] = taux.euro
            request.session['taux_gnf'] = taux.gnf
        response = self.get_response(request)
        return response
