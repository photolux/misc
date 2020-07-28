import os
import argparse
from zipfile import ZipFile


def parse_args():
    parser = argparse.ArgumentParser(description="Compress .eps and .jpg files into zip archives.")
    parser.add_argument("--input", dest="input_folder", default=".")
    parser.add_argument("--output", dest="output_folder", default=".")
    return parser.parse_args()


class App:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def get_index_from_filename(self, filename):
        return filename.split("/")[-1].split(".")[0]

    def zip_pairs(self, pairs):
        for index in pairs:
            if not os.path.isdir(self.output_folder):
                print(f"Creating output directory: {self.output_folder}...")
                os.mkdir(self.output_folder)

            output_path = os.path.join(self.output_folder, f'{index}.zip')
            if os.path.isfile(output_path):
                print(f"File {output_path} already exists. Skipping...")
                continue

            with ZipFile(output_path, 'w') as zip:
                file_1 = pairs[index].pop()
                file_2 = pairs[index].pop()
                zip.write(file_1, os.path.basename(file_1))
                zip.write(file_2, os.path.basename(file_2))
                print(f"Writing file {output_path}")


    def get_file_pairs(self, input_folder):
        tmp = {}
        result = {}
        filenames = filter(os.path.isfile, [os.path.join(input_folder, f) for f in os.listdir(input_folder)])
        for filename in filenames:
            index = self.get_index_from_filename(filename)
            if index not in tmp:
                tmp[index] = set([filename])
            else:
                tmp[index].add(filename)

        for index in tmp:
            if len(tmp[index]) == 2:
                result[index] = tmp[index]

        return result

    def run(self):
        print("Getting file pairs...")
        pairs = self.get_file_pairs(self.input_folder)
        self.zip_pairs(pairs)
        print("done.")


def main():
    args = parse_args()

    app = App(args.input_folder, args.output_folder)
    app.run()


if __name__ == "__main__":
    main()
