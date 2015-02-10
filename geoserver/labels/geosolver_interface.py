from geosolver.diagram.states import Label, LabeledImage
from geosolver.ontology.instantiator_definitions import instantiators

__author__ = 'minjoon'

def get_labeled_image(image, label_array):
    labels = {}
    for key, label_dict in enumerate(label_array):
        x = label_dict['x']
        y = label_dict['y']
        label_string = label_dict['label']
        type_ = label_dict['type']
        label = Label(label_string, instantiators['point'](x, y))
        labels[key] = label
    labeled_image = LabeledImage(image, labels)
    return labeled_image.get_labeled_image()

