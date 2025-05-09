
from import_export.formats import base_formats

def export_multiple_resources(querysets, format='csv'):
    datasets = []

    for queryset, resource_class in querysets:
        resource = resource_class()
        dataset = resource.export(queryset)
        datasets.append(dataset)

    combined_dataset = base_formats.CSV() if format == 'csv' else base_formats.XLSX()
    for dataset in datasets:
        combined_dataset.append(dataset.dict)

    return combined_dataset

