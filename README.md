
# Simple VPC Stack

Bienvenidos a mi proyecto de infraestructura en la nube de AWS. En este proyecto he creado los siguientes recursos dentro de una región de AWS:

* 1 VPC (Virtual Private Cloud) para aislar lógicamente los recursos.

* 2 subnets privadas dentro del VPC para alojar recursos que no requieran acceso a internet como bases de datos.

* 2 subnets públicas dentro del VPC para alojar recursos que sí requieran acceso a internet como servidores web. Cada una de estas subnets públicas tiene asociada un NAT Gateway para permitir la navegación saliente hacia internet desde las subnets privadas.

* 1 Internet Gateway asociado al VPC para permitir la comunicación entre los recursos de las subnets públicas y internet.

Las tablas de rutas necesarias para dirigir el tráfico entre las subnets privadas, públicas e internet.

Parámetros almacenados en Parameter Store para guardar los IDs de los recursos creados. Estos parámetros podrán ser utilizados por otros stacks de CloudFormation para recuperar los IDs y realizar referencias cruzadas entre stacks.


![simple vpc two az, private and public subnets](/vpc.jpg)

el codigo es bastante simple


```python
from aws_cdk import Stack, CfnOutput, aws_ec2 as ec2, aws_ssm as ssm
from constructs import Construct


class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "V", max_azs=2)
        private_subnets = vpc.private_subnets
        public_subnets = vpc.public_subnets

        private_subnets_ids = ",".join([sn.subnet_id for sn in private_subnets])
        public_subnets_ids = ",".join([sn.subnet_id for sn in public_subnets])

        self.create_ssm_param("vpc-id", vpc.vpc_id)
        self.create_ssm_param("vpc-azs", ",".join(vpc.availability_zones))
        self.create_ssm_param("vpc-private-subnets", private_subnets_ids)
        self.create_ssm_param("vpc-public-subnets", public_subnets_ids)

```



## Instrucciones para despliegue

A continuación encuentras las instrucciones para desplegar este proyecto (verifica tus [limites de servicio](https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html) previamente)



```zsh
git clone https://github.com/ensamblador/simple-vpc.git
cd simple-vpc
python3 -m venv .venv
```

en linux o macos el ambiente se activa así:

```zsh
source .venv/bin/activate
```

en windows

```cmd
% .venv\Scripts\activate.bat
```

Una vez activado instalamos las dependencias
```zsh
pip install -r requirements.txt
```

en este punto ya se puede desplegar:

```zsh
cdk deploy
```

y para eliminar:

```zsh
cdk destroy
```


## Otros comandos útiles

 * `cdk synth`       crea un template de cloudformation con los recursos de este proyecto
 * `cdk diff`        compara el stack desplegado con el nuevo estado local

Enjoy!
