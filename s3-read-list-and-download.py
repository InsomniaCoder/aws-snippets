import os
with open("filename.txt") as file_in:
    for line in file_in:
        s3_download_cmd = "aws s3 cp s3://{bucket-name}/" + line.rstrip("\n") + " " + line.rstrip("\n") + " --profile={profile}"
        os.system(s3_download_cmd)
