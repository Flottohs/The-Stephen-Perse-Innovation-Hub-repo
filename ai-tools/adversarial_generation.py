from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import torch

import torch
import torch.nn as nn

from torchvision.transforms.functional import to_pil_image

def save_adv_image(x_adv, filename="adv.png"):
    # Remove batch dimension
    img = x_adv.squeeze(0)

    # Convert from [-1,1] → [0,1]
    img = (img + 1) / 2

    # Clamp to valid range
    img = img.clamp(0, 1)

    # Convert to PIL image
    pil_img = to_pil_image(img.cpu())

    # Save
    pil_img.save(filename)

def generate_adversarial_example(model, image, label, epsilon):
    """
    model: ViTForImageClassification
    image: tensor of shape [1, 3, 224, 224]
    label: int (correct class index)
    epsilon: perturbation size
    """
    model.eval()

    # Ensure gradient tracking
    image = image.clone().detach().requires_grad_(True)

    # Forward pass
    outputs = model(pixel_values=image)
    logits = outputs.logits

    loss = nn.CrossEntropyLoss()(logits, torch.tensor([label], device=image.device))

    # Backward pass
    model.zero_grad()
    loss.backward()

    # FGSM step
    perturbation = epsilon * image.grad.sign()
    adversarial_image = image + perturbation

    # Clamp to valid range
    adversarial_image = torch.clamp(adversarial_image, -1, 1)

    return adversarial_image.detach()

# Load model
model = ViTForImageClassification.from_pretrained(
    "google/vit-base-patch16-224"
)

processor = ViTImageProcessor.from_pretrained(
    "google/vit-base-patch16-224"
)

# Load image
image = Image.open("closeup.jpg").convert("RGB")
inputs = processor(images=image, return_tensors="pt")

x = inputs["pixel_values"]

# Get true label
with torch.no_grad():
    logits = model(pixel_values=x).logits
    label = logits.argmax(dim=1).item()

# Generate adversarial image
x_adv = generate_adversarial_example(model, x, label, epsilon=0.03)
save_adv_image(x_adv, "adversarial_closeup.png")
