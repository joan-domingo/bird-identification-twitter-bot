import argparse
import pathlib
import numpy as np
import tensorflow
import PIL.Image
from read_bird_list import read_scientific_name


# run file with: python predict.py <model_path> <test_image_path>


class Model:
    def __init__(self, model_filepath):
        self.graph_def = tensorflow.compat.v1.GraphDef()
        self.graph_def.ParseFromString(model_filepath.read_bytes())

        input_names, self.output_names = self._get_graph_inout(self.graph_def)
        assert len(input_names) == 1
        self.input_name = input_names[0]
        self.input_shape = self._get_input_shape(self.graph_def, self.input_name)

    def predict(self, image_filepath):
        image = PIL.Image.open(image_filepath).resize(self.input_shape)
        input_array = np.array(image, dtype=np.float32)[np.newaxis, :, :, :]

        with tensorflow.compat.v1.Session() as sess:
            tensorflow.import_graph_def(self.graph_def, name='')
            out_tensors = [sess.graph.get_tensor_by_name(o + ':0') for o in self.output_names]
            outputs = sess.run(out_tensors, {self.input_name + ':0': input_array})

        return {name: outputs[i] for i, name in enumerate(self.output_names)}

    @staticmethod
    def _get_graph_inout(graph_def):
        input_names = []
        inputs_set = set()
        outputs_set = set()

        for node in graph_def.node:
            if node.op == 'Placeholder':
                input_names.append(node.name)

            for i in node.input:
                inputs_set.add(i.split(':')[0])
            outputs_set.add(node.name)

        output_names = list(outputs_set - inputs_set)
        return input_names, output_names

    @staticmethod
    def _get_input_shape(graph_def, input_name):
        for node in graph_def.node:
            if node.name == input_name:
                return [dim.size for dim in node.attr['shape'].shape.dim][1:3]


def print_outputs(outputs):
    outputs = list(outputs.values())[0]

    #for index, score in enumerate(outputs[0]):
    #    print(f"Label: {index}, score: {score:.5f}")


    labels = []
    labels_file = open('model/labels.txt', 'r')
    for label in labels_file.readlines():
        labels.append(label.strip())

    highest_score = np.max(outputs[0])
    first_class = labels[np.argmax(outputs[0])]
    first_class_scientific_name = read_scientific_name(first_class)
    print(f"Specie {first_class} ({first_class_scientific_name}) with score of {highest_score}")


    second_highest = 0
    second_position = -1;
    for i, score in enumerate(outputs[0]):
        if score > second_highest and score < highest_score:
            second_highest = score
            second_position = i

    second_class = labels[second_position]
    second_class_scientific_name = read_scientific_name(second_class)
    print(f"Specie {second_class} ({second_class_scientific_name}) with score of {second_highest}")

    third_highest = 0
    third_position = -1;
    for i, score in enumerate(outputs[0]):
        if score > third_highest and score < second_highest:
            third_highest = score
            third_position = i

    third_class = labels[third_position]
    third_class_scientific_name = read_scientific_name(third_class)
    print(f"Specie {third_class} ({third_class_scientific_name}) with score of {third_highest}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model_filepath', type=pathlib.Path)
    parser.add_argument('image_filepath', type=pathlib.Path)

    args = parser.parse_args()

    model = Model(args.model_filepath)
    outputs = model.predict(args.image_filepath)
    print_outputs(outputs)


if __name__ == '__main__':
    main()