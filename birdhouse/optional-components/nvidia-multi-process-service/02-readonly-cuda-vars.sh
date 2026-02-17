# Make these two variables that set limits readonly so that users cannot overwrite
# these variables from inside their jupyterlab container.
readonly CUDA_MPS_PINNED_DEVICE_MEM_LIMIT
readonly CUDA_MPS_ACTIVE_THREAD_PERCENTAGE
