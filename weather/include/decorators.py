from django.utils.encoding import uri_to_iri


def iri_url(function):
    def wrap(request, *args, **kwargs):
        if 'country' in kwargs:
            kwargs['country'] = uri_to_iri(kwargs['country'])

        if 'voivodeship' in kwargs:
            kwargs['voivodeship'] = uri_to_iri(kwargs['voivodeship'])

        if 'county' in kwargs:
            kwargs['county'] = uri_to_iri(kwargs['county'])

        return function(request, *args, **kwargs)
    return wrap
