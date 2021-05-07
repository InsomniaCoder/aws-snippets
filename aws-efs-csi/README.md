# EFS CSI Driver

This part demonstrate how you can use EFS as Persistent Volume for your pods in Kubernetes cluster

First you need to install efs-csi-driver into your `kube-system` namespace in your cluster

https://github.com/kubernetes-sigs/aws-efs-csi-driver

2 main installation steps are:

1. add this policy to your IAM profile that you attached to the EC2 K8s Node

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "elasticfilesystem:DescribeAccessPoints",
        "elasticfilesystem:DescribeFileSystems"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "elasticfilesystem:CreateAccessPoint"
      ],
      "Resource": "*",
      "Condition": {
        "StringLike": {
          "aws:RequestTag/efs.csi.aws.com/cluster": "true"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": "elasticfilesystem:DeleteAccessPoint",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/efs.csi.aws.com/cluster": "true"
        }
      }
    }
  ]
}
```

2. install efs-csi-driver using helm

```
helm repo add aws-efs-csi-driver https://kubernetes-sigs.github.io/aws-efs-csi-driver/
helm repo update
helm upgrade --install aws-efs-csi-driver --namespace kube-system aws-efs-csi-driver/aws-efs-csi-driver
```

you can check if it deploys successfully by get pods in your `kube-system` namespace.


Next step:

Create AWS EFS into your account within the same VPC  as your EKS or Bare metal kubernetes cluster and assign correct security group that allows your node to connect with EFS

Run `kuectl apply -f .` within this directory.

It will create

1. storage class: `efs-sc` with provisioner: `efs.csi.aws.com`
2. create PV that links to your EFS name : fs-xxxxxxx
3. create PVC for your application to use
4. create a deployment or pod and mount to that PVC