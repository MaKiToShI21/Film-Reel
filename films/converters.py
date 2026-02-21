class FourDigitYearConverter:
    regex = '[0-9]{4}'
    
    def to_python(self, value):
        return int(value)
    
    def to_url(self, value):
        return '%04d' % value


class RatingConverter:
    regex = '[1-9](\.[0-9])?|10\.0'
    
    def to_python(self, value):
        return float(value)
    
    def to_url(self, value):
        return f"{value:.1f}"
