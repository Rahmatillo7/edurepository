from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    if filesize > 50 * 1024 * 1024: # 50 MB limit
        raise ValidationError("Fayl hajmi 50MB dan oshmasligi kerak!")
    return value

# Resource modeling ichidagi 'file' maydoniga qo'shing:
# file = models.FileField(upload_to='resources/%Y/%m/', validators=[validate_file_size])
