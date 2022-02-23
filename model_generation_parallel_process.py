import os, sys, glob, re

def file_names(path1, d_name, ext1):
    '''
    files present in different directories and different folder can be named by this function
    path1: is file path
    d_name: is the folder where the required files are present
    ext1: is the extension of the required file
    '''
    file_location = os.path.join(path1, d_name, ext1)
    f_names = glob.glob(file_location)
    return(f_names)


## input alignment files directory
input_alignment_files1 = file_names('/home/aditi/Desktop/modeller_demo/all_2216_seqs_model_generation', 'curated_alignment_ali', '*.ali')
input_alignment_files1.sort()
input_alignment_files2 = input_alignment_files1[1058:]
input_alignment_files2.sort()
input_alignment_files3 = input_alignment_files1[1350:]
input_alignment_files3.sort()


##input seq_ids
all_ids = open("/home/aditi/Desktop/modeller_demo/all_2216_seqs_model_generation/all_ids.txt").read()
all_seqids1 = all_ids.split("\n")[0:-1]
all_seqids1.sort()                                                                                                ## for run1
all_seqids2 = all_seqids1[1058:]
all_seqids2.sort()                                                                                                ## for run2
all_seqids3 =  all_seqids1[1350:]
all_seqids3.sort()                                                                                                ## for run3


## making empty directories for output based on the seq_ids

## after crashing the job, all empty directories from the destination out_dir should be deleted, so that code will generate new direcories
directory = '/home/aditi/Desktop/modeller_demo/all_2216_seqs_model_generation/model_out_files'
for entry in os.scandir(directory):
    if os.path.isdir(entry.path) and not os.listdir(entry.path) :
        os.rmdir(entry.path)

## making empty directories for output based on the seq_ids
root_dir_path = '/home/aditi/Desktop/modeller_demo/all_2216_seqs_model_generation/model_out_files/'
for seq_id in all_seqids3:                                  # change according to the run number
    os.mkdir(os.path.join(root_dir_path,seq_id))

## reading file names of the outfiles
modeling_outfiles1 = os.listdir("/home/aditi/Desktop/modeller_demo/all_2216_seqs_model_generation/model_out_files")
modeling_outfiles1.sort()                                                                                           ## for run1
modeling_outfiles2 = modeling_outfiles1[1058:]
modeling_outfiles2.sort()                                                                                          ## for run2
modeling_outfiles3 = modeling_outfiles1[1350:]
modeling_outfiles3.sort()                                                                                          ## for run3

## zipped files for giving input for the function
modeller_inputs1 = list(zip(input_alignment_files1, all_seqids1, modeling_outfiles1))                              ## for run1
modeller_inputs2 = list(zip(input_alignment_files2, all_seqids2, modeling_outfiles2))                              ## for run2
modeller_inputs3 = list(zip(input_alignment_files3, all_seqids3, modeling_outfiles3))                              ## for run3


# Comparative modeling by the AutoModel class, using multiple processors
from modeller import *
from modeller.automodel import *    ## Load the AutoModel class
from modeller.parallel import Job, LocalWorker

def parallel_modelling(alignment_file, sequence_id, demo_outfiles):
    os.chdir('/home/aditi/Desktop/modeller_demo/all_2216_seqs_model_generation/model_out_files/{}'.format(demo_outfiles))
    ## Use 4 CPUs in a parallel job on this machine
    j = Job()
    j.append(LocalWorker())
    j.append(LocalWorker())
    j.append(LocalWorker())
    j.append(LocalWorker())


    log.verbose()    ## request verbose output
    env = Environ()  ## create a new MODELLER environment to build this model in

    ## directories for input atom files
    env.io.atom_files_directory = ['/home/aditi/Desktop/modeller_demo/all_2216_seqs_model_generation']

    a = AutoModel(env,
                  alnfile  = '{}'.format(alignment_file),     ## alignment filename
                  knowns   = '6i6b',                 ## codes of the templates
                  sequence = '{}'.format(sequence_id),
                  assess_methods= (assess.DOPE, assess.GA341))           ## code of the target


    # a.very_fast()                     ## to generate approximate models, 3 times faster
    a.starting_model= 1                 ## index of the first model
    a.ending_model  = 10                ## index of the last model ,
                                        ## (determines how many models to calculate)

    a.use_parallel_job(j)               ## Use the job for model building
    a.make()                            ## do the actual comparative modeling
     

# ##run1:
# for p, q, r in modeller_inputs:
#     parallel_modelling(p, q, r)


# ## run2: job crash after 1058 sequences due to alignment error, so run from 1058 sequence number
# for p, q, r in modeller_inputs2:
#     parallel_modelling(p, q, r)



## run3: job crashed after 1350 sequences due to alignment error so run from 1350 sequence number
for p, q, r in modeller_inputs3:
    parallel_modelling(p, q, r)
