from django import forms
from crispy_forms.layout import Layout, Div
from tom_observations.facility import GenericObservationFacility, GenericObservationForm

class APOForm(GenericObservationForm):
    name = forms.CharField()
    notes = forms.CharField()
    start = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    end = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}))
    exposure_count = forms.IntegerField(min_value=1)
    exposure_time = forms.FloatField(min_value=1)
    max_airmass = forms.FloatField()
    # pass
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['proposal'] = forms.ChoiceField(choices=self.proposal_choices())
        self.fields['priority']   = forms.ChoiceField(choices=self.priority_choices())
        self.fields['filter']     = forms.ChoiceField(choices=self.filter_choices())
        self.fields['instrument'] = forms.ChoiceField(choices=self.instrument_choices())
        self.helper.layout = Layout(
            self.common_layout,
            self.layout(),
            # self.extra_layout()
        )

    def layout(self):
        return Div(
            Div(
                'name', 'notes', 'priority', 'start', 'end',
                css_class='col'
            ),
            Div(
                'filter', 'instrument', 'exposure_count', 'exposure_time', 'max_airmass',
                css_class='col'
            ),
            css_class='form-row'
        )

    def instrument_choices(self):
        return set([('AGILE','AGILE'),('ARCES','ARCES'),('ARCTIC','ARCTIC'),
        	('DIS','DIS'),('NICFPS','NICFPS'),('TRIPLESPEC','TRIPLESPEC')])

    def filter_choices(self):
        return set([('J','J'),('H','H'),('K','K')])

    def priority_choices(self):
    	return [(1,'1 urgent'),(2,'2 high'),(3,'3 medium'),(4,'4 low'),(5,'5 backup')]


class APOImagingObservationForm(APOForm):
    def instrument_choices(self):
        return [('AGILE','AGILE'),('ARCTIC','ARCTIC'),('NICFPS','NICFPS')]

    def filter_choices(self):
        return set([('J','J'),('H','H'),('K','K')])



class APOSpectraObservationForm(APOForm):
    def instrument_choices(self):
        return [('ARCES','ARCES'),('DIS','DIS'),('NICFPS','NICFPS'),('TRIPLESPEC','TRIPLESPEC')]

    def filter_choices(self):
        return set([('J','J'),('H','H'),('K','K')])




class APOFacility(GenericObservationFacility):
    name = 'APO'
    observation_types = [('IMAGING', 'Imaging'), ('SPECTRA', 'Spectroscopy')]
    # observation_types = [('OBSERVATION', 'Custom Observation')]

    SITES = {
        'APO': {
            'sitecode': 'APO',
            'latitude': 32.780278,
            'longitude': 105.820278,
            'elevation': 2788
            },
        }

    def data_products(self, observation_id, product_id=None):
        return []

    def get_form(self, observation_type):
        return APOForm

    def get_observation_status(self, observation_id):
        return ['IN_PROGRESS']

    def get_observation_url(self, observation_id):
        return ''

    def get_observing_sites(self):
    	return self.SITES

    def get_terminal_observing_states(self):
        return ['IN_PROGRESS', 'COMPLETED']

    def submit_observation(self, observation_payload):
        print(observation_payload)
        return [1]

    def validate_observation(self, observation_payload):
        pass
