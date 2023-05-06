from pathlib import Path
from django.views.generic import TemplateView


def photo_list(gallery):
    def photo_details(i, f):
        return dict(id=i, file=f, name=f.name)

    path = f"static/images/MarkSeaman.org/photos/{gallery}"
    photos = [f for f in Path(path).iterdir() if not ".DS_Store" in str(f)]
    photos = [photo_details(i, f) for i, f in enumerate(photos)]
    return photos


class BrandingView(TemplateView):
    template_name = "branding.html"

    def get_context_data(self, **kwargs):
        return dict(photos=photo_list("static/images/MarkSeaman/sws-logo", "600"))


class PhotoListView(TemplateView):
    template_name = "photos.html"

    def get_context_data(self, **kwargs):
        gallery = kwargs["directory"]
        title = (
            "Colorado Mountains in Autumn" if gallery == "Colorado" else "Photo Gallery"
        )
        return dict(title=title, photos=photo_list(gallery), gallery=gallery)


class PhotoDetailView(TemplateView):
    template_name = "photo.html"

    def get_context_data(self, **kwargs):
        i = kwargs["id"]
        gallery = kwargs["directory"]
        photos = photo_list(gallery)
        p = photos[i]
        return dict(photo=p, gallery=gallery)
