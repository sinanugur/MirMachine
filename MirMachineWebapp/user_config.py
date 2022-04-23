# USER CONFIG FILE, SPECIFY PARAMETERS ACCORDING TO YOUR NEEDS

MAX_NCBI_GENOME_SIZE = 100000   # In bytes, legacy => Not used

SNAKEMAKE_CPU_NUM = 15          # Number of CPU threads used on jobs

AUTO_CLEANUP_TEMP_FILES = True

JOB_STATUS_UPDATE_FREQ = 20     # Sends update at every 100/20th percent, MAX 100

THROTTLE_JOB_SUBMIT = False
JOB_SUBMIT_THROTTLE_RATE = '1/m'    # 1 per minute

JOB_EXPIRATION_TIME = 2   # In days
