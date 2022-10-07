from collections import defaultdict

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


def follow(
    viewset, request, id, target_model, target_field: str, through_model
):
    target = get_object_or_404(target_model, pk=id)
    record = {
        target_field: target,
        'user': request.user,
    }
    through_model.objects.create(**record)
    serializer = viewset.get_serializer(target)
    return Response(serializer.data)


def unfollow(request, id, target_field: str, through_model):
    record = {
        target_field + '__id': id,
        'user': request.user,
    }
    subscription = get_object_or_404(through_model, **record)
    subscription.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def build_ingredients_summary(recipes_ingredients):
    summary = defaultdict(int)
    for ingredients in recipes_ingredients:
        for ingredient in ingredients:
            key = (ingredient['name'], ingredient['measurement_unit'])
            summary[key] += ingredient['amount']

    results = []
    for ingredient, amount in summary.items():
        name, measurement_unit = ingredient
        results.append(
            {
                'name': name,
                'amount': amount,
                'measurement_unit': measurement_unit,
            }
        )
    return results