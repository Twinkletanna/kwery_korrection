# kwery_korrection
IR project 646 UMass

Please read the report for more context. It also explains what each of the method does. The files are commented and proper references are present inside the .py files.

Each requires different versions of libraries. We would suggest to use miniconda environments. We ran on UMass gypsum clusters with GPU access (and the environment names we have used are in the comments of the py file). If you want to run the code, go to their requirements page and install it. Else shoot one of us an email.

There are 4 neural methods. Make sure you have GPUs to be fast (Even then it will take time). We couldn't train the whole of the tal character encoder RNN (and we put for 7 days).

There are .sh files also. If you just want to replicate our metrics, start by changing path names and running these scripts on gypsum as is.
