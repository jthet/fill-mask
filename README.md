# Fill-Mask
## Application for the 'fill-mask' ML model
A description of the fill-mask model can be found [here](https://huggingface.co/tasks/fill-mask).

This is an application that performs the Fill-mask mode using torch on an HPC system.

## Details 
The fill-mask model is a language model designed to predict missing words or phrases in a given sentence or text. It uses contextual information and training data to generate the most probable completion for the masked portion of the input.

This directory contains the `app.json` file to define the application using the docker image [jthet/fill_mask_app:latest](https://hub.docker.com/repository/docker/jthet/fill_mask_app/general).

The `job.json` defines the jobs definition to be submitted to the HPC cluster through a client. 

The `job.json` file takes in two arguments; the sentance with the masked word and the number of outputs. 

For example, the following arguments:
```
{
    "name": "fill-mask-job",
    "appId": "fill-mask-jacksont",
    "appVersion": "0.1.0",
    "execSystemId": "<system name>",
    "parameterSet": {
        "appArgs": [
            {
                "arg": " \"The goal of life is <mask>.\" " 
            },
            {
                "arg": "2"
            }
        ]
    }
}
```

Return the following output in `fill-mask-output/output.txt`:

```
{'score': 0.06897135078907013, 'token': 11098, 'token_str': ' happiness', 'sequence': 'The goal of life is happiness.'}
{'score': 0.06554921716451645, 'token': 45075, 'token_str': ' immortality', 'sequence': 'The goal of life is immortality.'}
{'score': 0.032357435673475266, 'token': 14314, 'token_str': ' yours', 'sequence': 'The goal of life is yours.'}
{'score': 0.02431384101510048, 'token': 22211, 'token_str': ' liberation', 'sequence': 'The goal of life is liberation.'}
```



