from django import forms

from .models import Listings, WatchList


class AddItemsForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = [
            "title",
            "description",
            "start_price",
            "category",
            "image",
        ]


class WatchListForm(forms.ModelForm):
    class Meta:
        model = WatchList
        fields = [
            "user_id",
            "item_id",
        ]