# End-to-End-Basketball-QA-RAG-Capstone

## Loading the model
base_model_name = "unsloth/Llama-3.2-3B-Instruct"
adapter_path = "/content/drive/MyDrive/Capstone Project Model Weights/best_model_r8_alpha8_dropout0.05_lr5e-05"  
max_seq_length = 2048

#Load base model
base_model, _ = FastLanguageModel.from_pretrained(
    model_name=base_model_name,
    max_seq_length=max_seq_length,
    load_in_4bit=True,
)

#Load trained adapter
model = PeftModel.from_pretrained(base_model, adapter_path)

#Load tokenizer from saved directory
tokenizer = AutoTokenizer.from_pretrained(adapter_path)

## Model Quantization

model.save_pretrained_gguf("model", tokenizer, quantization_method="not_quantized")
#Model weights are 16-bit floating-point precision (FP16).

## Inference on ollama

Created Modelfile_llama3.2 for inferencing on ollama
Experimented with different hyperparameters to check quality of inference.
Notable hyperparameters:
- Temperature: The temperature of the model. Increasing the temperature will make the model answer more creatively.
- num_predict: Maximum number of tokens to predict when generating text.
- seed: Sets the random number seed to use for generation. Setting this to a specific number will make the model generate the same text for the same prompt.

Experimented with 7 different versions of Modelfile, tried different hyperparameters like StopParameters. I also tried using adapter weights (safe tensors) along with model weights (gguf). But the inference quality was not good.

Documentation: https://github.com/ollama/ollama/blob/main/docs/modelfile.md

```bash
ollama create finetunedllama3.2ParamExp2 -f ./Modelfile_llama3.2
ollama run finetunedllama3.2ParamExp2
```
## Exposing public URL using ngrok
```bash
ollama serve
ngrok http 11434 --host-header=localhost
```

## Test Command
### Local Test
```bash
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "finetunedllama3.2ParamExp2",
  "prompt": "What is the number of players on the Chicago Bulls who are 25 years old or younger?",
  "stream": false
}'
```
### Testing on public url
Model live at: https://5b33-2601-19b-e02-2da0-c46f-e889-1ca5-5f25.ngrok-free.app/api/generate (On Apple M3 16GB)

<img width="1025" alt="image" src="https://github.com/user-attachments/assets/9c6eaf90-5597-48bb-a76d-15cfb78a9127" />

## Model Weights
Link to model weights: https://drive.google.com/drive/folders/1ocAiCka81Ug905IH7lMAHo9o73CMt-5o?usp=sharing


