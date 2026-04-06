from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    if filesize > 50 * 1024 * 1024: # 50 MB
        raise ValidationError("Fayl hajmi 50MB dan oshmasligi kerak!")
    return value

# file = models.FileField(upload_to='...', validators=[validate_file_size])
