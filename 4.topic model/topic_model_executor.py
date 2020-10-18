# java -jar out/artifacts/PK_STTM_jar/PK-STTM.jar -model PKLFLDA -ntopics 24 -alpha 0.2 -beta 0.01 -niters 1 -twords 10 -name TEST-ALPHA-COMBINED -mu 0.7 -sigma 0.3 -A 25 -ks ../Goto-7.1/result\ Source\ LDA/12aug_7.1_BK.csv.dat-KS.dat -corpus ../Goto-7.1/result\ Source\ LDA/hyp_1aug_7.1.csv-READY.dat -gt ../Goto-7.1/result\ Source\ LDA/gt.dat
# ./src_lda 	-g \
# 		 	-out=../tests/reuters \
# 		 	-ks=../data/reuters/ks.dat \
# 		 	-P=7 | tee ../tests/reuters/output.log

import argparse
import os

# Retrieve Input
parser = argparse.ArgumentParser(description="Implement BK-LFLDA topic model to dialog dataset with background knowledge")
parser.add_argument("-dialog", required=True, type=str, help="Dialog file location. Please input full path but without extention. [default:]")
parser.add_argument("-bk", required=True, type=str, help="Background Knowledge file location. Please input the already augmented file. Please input full path but without extention. [default:]")
args = parser.parse_args()

ntopics = 0
with open(args.bk, "r") as f:
    ntopics = len(f.readlines())


#Generate Ground Truth Points
dialog_file_name = args.dialog.split("/")[-1].split(".")[0]
os.system("mkdir {}".format(dialog_file_name))
os.system("./src_lda -g -out={} -ks={} -P=7".format(dialog_file_name, args.bk))

#Execute BK-LFLDA (can be called PKLFLDA interchangeably)
os.system("java -jar PK-STTM.jar -model PKLFLDA -ntopics {} -alpha 0.15 -beta 0.01 -niters 2000 -twords 10 -name {} -mu 0.7 -sigma 0.3 -A 25 -ks {} -corpus {} -gt {} -lambda 0.4".format(ntopics, dialog_file_name, args.bk, args.dialog, "{}/gt.dat".format(dialog_file_name)))