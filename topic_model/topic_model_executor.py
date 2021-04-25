import os
import datetime

def execute(dataset_file, dataset_folder, background_file, ntopics):
    print("Begin executing topic model for {}...".format(dataset_folder))
    time_folder = "dataset/{}/{}".format(dataset_folder, str(datetime.datetime.now()).replace(" ", "_"))
    os.system("mkdir {}".format(time_folder))

    #Generate Ground Truth Points
    os.system("./topic_model/src_lda -g -out={} -ks={} -P=7".format(time_folder, background_file))

    #Execute BK-LFLDA (or PKLFLDA, both can be used interchangeably)
    os.system("java -jar topic_model/PK-STTM.jar -model PKLFLDA -ntopics {} -alpha 0.15 -beta 0.01 -niters 2000 -twords 10 -name {} -mu 0.7 -sigma 0.3 -A 25 -ks {} -corpus {} -gt {} -lambda 0.4".format(ntopics, dataset_folder, background_file, dataset_file, time_folder+"/gt.dat"))

    #Move results to dataset folder
    os.system("mv results {}/".format(time_folder))
    print("Finish executing topic model for {}!".format(dataset_folder))
    return time_folder+"/results/"
