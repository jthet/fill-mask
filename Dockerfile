# Image: jthet/fill_mask_app
# Run with:
#   docker run jthet/fill_mask_app:latest

FROM huggingface/transformers-pytorch-cpu:4.18.0

COPY unmasker.py /app/unmasker.py

ENTRYPOINT [ "python3", "/app/unmasker.py" ]

