import pandas as pd
import argparse

def run_merge_sentence(dataset, column, column_pivot):
    # Sanitize input
    file_name = dataset
    if "/" in file_name:
        file_name = " ".join(dataset.split("/")[-1].split(".")[:-1])

    # Open file
    dataset_df = pd.read_csv(dataset)
    dataset_df = dataset_df.groupby([column_pivot])[column].apply(' '.join).reset_index()

    with open("[MERGED]"+file_name+".csv", 'w') as f:
        f.write(column_pivot + "," + column + "\n")

        for _,d in dataset_df.iterrows():
            combined_sentence = d[column]
            combined_sentence = combined_sentence.replace("\"", " ")
            combined_sentence = "\"" + combined_sentence + "\""

            f.write(str(d[column_pivot]) + ',' + combined_sentence + "\n")

    print("Merging success!!")

# Retrieve Input
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-dataset", required=True, type=str)
    parser.add_argument("-column", required=True, type=str)
    parser.add_argument("-column_pivot", required=True, type=str)
    args = parser.parse_args()

    run_merge_sentence(args.dataset, args.column, args.column_pivot)

if __name__ == "__main__":
    main()