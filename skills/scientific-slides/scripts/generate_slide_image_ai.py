#!/usr/bin/env python3
"""
AI-powered slide image generation using Nano Banana Pro.

This script generates presentation slides or slide visuals using AI:
- full_slide mode: Generate complete slides with title, content, and visuals (for PDF workflow)
- visual_only mode: Generate just images/figures to place on slides (for PPT workflow)

Supports attaching reference images for context (e.g., "create a slide about this chart").

Uses smart iterative refinement:
1. Generate initial image with Nano Banana Pro
2. Quality review using Gemini 3 Pro
3. Only regenerate if quality is below threshold
4. Repeat until quality meets standards (max iterations)

Requirements:
    - OPENROUTER_API_KEY environment variable
    - requests library

Usage:
    # Full slide for PDF workflow
    python generate_slide_image_ai.py "Title: Introduction to ML\nKey points: supervised learning, neural networks" -o slide_01.png

    # Visual only for PPT workflow
    python generate_slide_image_ai.py "Neural network architecture diagram" -o figure.png --visual-only

    # With reference images attached
    python generate_slide_image_ai.py "Create a slide explaining this chart" -o slide.png --attach chart.png --attach logo.png
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from dotenv import load_dotenv


def _load_env_file() -> bool:
    """Load .env file from current directory, parent directories, or package directory.

    Returns:
        bool: True if a .env file was found and loaded, False otherwise.
    """
    # Try current working directory first
    env_path: Path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)
        return True

    # Try parent directories (up to 5 levels)
    cwd: Path = Path.cwd()
    for _ in range(5):
        env_path = cwd / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return True
        cwd = cwd.parent
        if cwd == cwd.parent:
            break

    # Try the package's parent directory
    script_dir: Path = Path(__file__).resolve().parent
    for _ in range(5):
        env_path = script_dir / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return True
        script_dir = script_dir.parent
        if script_dir == script_dir.parent:
            break

    return False


class SlideImageGenerator:
    """Generate presentation slides or visuals using AI with iterative refinement.

    Two modes:
    - full_slide: Generate complete slide with title, content, visuals (for PDF workflow)
    - visual_only: Generate just the image/figure for a slide (for PPT workflow)

    Attributes:
        QUALITY_THRESHOLD (float): Quality threshold for presentations.
        FULL_SLIDE_GUIDELINES (str): Guidelines for generating full slides.
        VISUAL_ONLY_GUIDELINES (str): Guidelines for generating slide visuals only.
    """

    # Quality threshold for presentations (lower than journal/conference papers)
    QUALITY_THRESHOLD: float = 6.5

    # Guidelines for generating full slides (complete slide images)
    FULL_SLIDE_GUIDELINES: str = """
Create a professional presentation slide image with these requirements:

SLIDE LAYOUT (16:9 aspect ratio):
- Clean, modern slide design
- Clear visual hierarchy: title at top, content below
- Generous margins (at least 5% on all sides)
- Balanced composition with intentional white space

TYPOGRAPHY:
- LARGE, bold title text (easily readable from distance)
- Clear, sans-serif fonts throughout
- High contrast text (dark on light or light on dark)
- Bullet points or key phrases, NOT paragraphs
- Maximum 5-6 lines of text content
- Default author/presenter: "K-Dense" (use this unless another name is specified)

VISUAL ELEMENTS:
- Use GENERIC, simple images and icons - avoid overly specific or detailed imagery
- MINIMAL extra elements - no decorative borders, shadows, or flourishes
- Visuals should support and enhance the message, not distract
- Professional, clean aesthetic with restraint
- Consistent color scheme (2-3 main colors only)
- Prefer abstract/conceptual visuals over literal representations

PROFESSIONAL MINIMALISM:
- Less is more: favor empty space over additional elements
- No unnecessary decorations, gradients, or visual noise
- Clean lines and simple shapes
- Focused content without visual clutter
- Corporate/academic level of professionalism

PRESENTATION QUALITY:
- Designed for projection (high contrast)
- Bold, impactful design that commands attention
- Professional and polished appearance
- No cluttered or busy layouts
- Consistent styling throughout the deck
"""

    # Guidelines for generating slide visuals only (figures/images for PPT)
    VISUAL_ONLY_GUIDELINES: str = """
Create a high-quality visual/figure for a presentation slide:

IMAGE QUALITY:
- Clean, professional appearance
- High resolution and sharp details
- Suitable for embedding in a slide

DESIGN:
- Simple, clear composition with MINIMAL elements
- High contrast for projection readability
- No text unless essential to the visual
- Transparent or white background preferred
- GENERIC imagery - avoid overly specific or detailed visuals

PROFESSIONAL MINIMALISM:
- Favor simplicity over complexity
- No decorative elements, shadows, or flourishes
- Clean lines and simple shapes only
- Remove any unnecessary visual noise
- Abstract/conceptual rather than literal representations

STYLE:
- Modern, professional aesthetic
- Colorblind-friendly colors
- Bold but restrained imagery
- Suitable for scientific/professional presentations
- Corporate/academic level of polish
"""

    def __init__(self, api_key: Optional[str] = None, verbose: bool = False) -> None:
        """Initialize the generator.

        Args:
            api_key (Optional[str]): OpenRouter API key (or use OPENROUTER_API_KEY env var).
            verbose (bool): Print detailed progress information.

        Raises:
            ValueError: If the OpenRouter API key is not found.
        """
        self.api_key: Optional[str] = api_key or os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            _load_env_file()
            self.api_key = os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found. Please either:\n"
                "  1. Set the OPENROUTER_API_KEY environment variable\n"
                "  2. Add OPENROUTER_API_KEY to your .env file\n"
                "  3. Pass api_key parameter to the constructor\n"
                "Get your API key from: https://openrouter.ai/keys"
            )

        self.verbose: bool = verbose
        self._last_error: Optional[str] = None
        self.base_url: str = "https://openrouter.ai/api/v1"
        # Nano Banana Pro for image generation
        self.image_model: str = "google/gemini-3-pro-image-preview"
        # Gemini 3 Pro for quality review
        self.review_model: str = "google/gemini-3-pro"

    def _log(self, message: str) -> None:
        """Log message if verbose mode is enabled.

        Args:
            message (str): The message to log.
        """
        if self.verbose:
            print(f"[{time.strftime('%H:%M:%S')}] {message}")

    def _make_request(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        modalities: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Make a request to OpenRouter API.

        Args:
            model (str): Model identifier.
            messages (List[Dict[str, Any]]): List of message dictionaries.
            modalities (Optional[List[str]]): Optional list of modalities (e.g., ["image", "text"]).

        Returns:
            Dict[str, Any]: API response as dictionary.

        Raises:
            RuntimeError: If the API request fails or times out.
        """
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/scientific-writer",
            "X-Title": "Scientific Slide Generator",
        }

        payload: Dict[str, Any] = {"model": model, "messages": messages}

        if modalities:
            payload["modalities"] = modalities

        self._log(f"Making request to {model}...")

        try:
            response: requests.Response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120,
            )

            try:
                response_json: Dict[str, Any] = response.json()
            except json.JSONDecodeError:
                response_json = {"raw_text": response.text[:500]}

            if response.status_code != 200:
                error_detail: Any = response_json.get("error", response_json)
                self._log(f"HTTP {response.status_code}: {error_detail}")
                raise RuntimeError(
                    f"API request failed (HTTP {response.status_code}): {error_detail}"
                )

            return response_json
        except requests.exceptions.Timeout:
            raise RuntimeError("API request timed out after 120 seconds")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")

    def _extract_image_from_response(self, response: Dict[str, Any]) -> Optional[bytes]:
        """Extract base64-encoded image from API response.

        Args:
            response (Dict[str, Any]): API response dictionary.

        Returns:
            Optional[bytes]: Image bytes or None if not found.
        """
        try:
            choices: List[Dict[str, Any]] = response.get("choices", [])
            if not choices:
                self._log("No choices in response")
                return None

            message: Dict[str, Any] = choices[0].get("message", {})

            # Nano Banana Pro returns images in the 'images' field
            images: List[Dict[str, Any]] = message.get("images", [])
            if images and len(images) > 0:
                self._log(f"Found {len(images)} image(s) in 'images' field")

                first_image: Dict[str, Any] = images[0]
                if isinstance(first_image, dict):
                    if first_image.get("type") == "image_url":
                        url: Any = first_image.get("image_url", {})
                        if isinstance(url, dict):
                            url = url.get("url", "")

                        if url and url.startswith("data:image"):
                            if "," in url:
                                base64_str: str = url.split(",", 1)[1]
                                base64_str = (
                                    base64_str.replace("\n", "")
                                    .replace("\r", "")
                                    .replace(" ", "")
                                )
                                self._log(
                                    f"Extracted base64 data (length: {len(base64_str)})"
                                )
                                return base64.b64decode(base64_str)

            # Fallback: check content field
            content: Any = message.get("content", "")

            if isinstance(content, str) and "data:image" in content:
                import re

                match = re.search(
                    r"data:image/[^;]+;base64,([A-Za-z0-9+/=\n\r]+)",
                    content,
                    re.DOTALL,
                )
                if match:
                    base64_str = (
                        match.group(1)
                        .replace("\n", "")
                        .replace("\r", "")
                        .replace(" ", "")
                    )
                    self._log(
                        f"Found image in content field (length: {len(base64_str)})"
                    )
                    return base64.b64decode(base64_str)

            if isinstance(content, list):
                for i, block in enumerate(content):
                    if isinstance(block, dict) and block.get("type") == "image_url":
                        url = block.get("image_url", {})
                        if isinstance(url, dict):
                            url = url.get("url", "")
                        if url and url.startswith("data:image") and "," in url:
                            base64_str = (
                                url.split(",", 1)[1]
                                .replace("\n", "")
                                .replace("\r", "")
                                .replace(" ", "")
                            )
                            self._log(f"Found image in content block {i}")
                            return base64.b64decode(base64_str)

            self._log("No image data found in response")
            return None

        except Exception as e:
            self._log(f"Error extracting image: {str(e)}")
            return None

    def _image_to_base64(self, image_path: str) -> str:
        """Convert image file to base64 data URL.

        Args:
            image_path (str): Path to image file.

        Returns:
            str: Base64 data URL string.
        """
        with open(image_path, "rb") as f:
            image_data: bytes = f.read()

        ext: str = Path(image_path).suffix.lower()
        mime_type: str = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }.get(ext, "image/png")

        base64_data: str = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{base64_data}"

    def generate_image(
        self, prompt: str, attachments: Optional[List[str]] = None
    ) -> Optional[bytes]:
        """Generate an image using Nano Banana Pro.

        Args:
            prompt (str): Text description of the image to generate.
            attachments (Optional[List[str]]): Optional list of image file paths
                to attach as context.

        Returns:
            Optional[bytes]: Image bytes or None if generation failed.
        """
        self._last_error = None

        # Build content with text and optional image attachments
        content: List[Dict[str, Any]] = []

        # Add text prompt
        content.append({"type": "text", "text": prompt})

        # Add attached images as context
        if attachments:
            for img_path in attachments:
                try:
                    img_data_url: str = self._image_to_base64(img_path)
                    content.append(
                        {"type": "image_url", "image_url": {"url": img_data_url}}
                    )
                    self._log(f"Attached image: {img_path}")
                except Exception as e:
                    self._log(f"Warning: Could not attach {img_path}: {e}")

        messages: List[Dict[str, Any]] = [
            {"role": "user", "content": content if attachments else prompt}
        ]

        try:
            response: Dict[str, Any] = self._make_request(
                model=self.image_model, messages=messages, modalities=["image", "text"]
            )

            if self.verbose:
                self._log(f"Response keys: {response.keys()}")
                if "error" in response:
                    self._log(f"API Error: {response['error']}")

            if "error" in response:
                error_msg: Any = response["error"]
                if isinstance(error_msg, dict):
                    error_msg = error_msg.get("message", str(error_msg))
                self._last_error = f"API Error: {error_msg}"
                print(f"✗ {self._last_error}")
                return None

            image_data: Optional[bytes] = self._extract_image_from_response(response)
            if image_data:
                self._log(f"✓ Generated image ({len(image_data)} bytes)")
            else:
                self._last_error = "No image data in API response"
                self._log(f"✗ {self._last_error}")

            return image_data
        except RuntimeError as e:
            self._last_error = str(e)
            self._log(f"✗ Generation failed: {self._last_error}")
            return None
        except Exception as e:
            self._last_error = f"Unexpected error: {str(e)}"
            self._log(f"✗ Generation failed: {self._last_error}")
            return None

    def review_image(
        self,
        image_path: str,
        original_prompt: str,
        iteration: int,
        visual_only: bool = False,
        max_iterations: int = 2,
    ) -> Tuple[str, float, bool]:
        """Review generated image using Gemini 3 Pro.

        Args:
            image_path (str): Path to the generated image.
            original_prompt (str): Original user prompt.
            iteration (int): Current iteration number.
            visual_only (bool): Whether evaluating just the visual or a full slide.
            max_iterations (int): Maximum allowed iterations.

        Returns:
            Tuple[str, float, bool]: Tuple of (critique, score, needs_improvement).
        """
        image_data_url: str = self._image_to_base64(image_path)
        threshold: float = self.QUALITY_THRESHOLD

        image_type: str = "slide visual/figure" if visual_only else "presentation slide"

        review_prompt: str = f"""You are an expert reviewer evaluating a {image_type} for presentation quality.

ORIGINAL REQUEST: {original_prompt}

QUALITY THRESHOLD: {threshold}/10
ITERATION: {iteration}/{max_iterations}

Evaluate this {image_type} on these criteria:

1. **Visual Impact** (0-2 points)
   - Bold, attention-grabbing design
   - Professional appearance
   - Suitable for projection

2. **Clarity** (0-2 points)
   - Easy to understand at a glance
   - Clear visual hierarchy
   - Not cluttered or busy

3. **Readability** (0-2 points)
   - Text is large and readable (if present)
   - High contrast
   - Clean typography

4. **Composition** (0-2 points)
   - Balanced layout
   - Good use of space
   - Appropriate margins

5. **Relevance** (0-2 points)
   - Matches the requested content
   - Appropriate style for presentations
   - Professional quality

RESPOND IN THIS EXACT FORMAT:
SCORE: [total score 0-10]

STRENGTHS:
- [strength 1]
- [strength 2]

ISSUES:
- [issue 1 if any]
- [issue 2 if any]

VERDICT: [ACCEPTABLE or NEEDS_IMPROVEMENT]

If score >= {threshold}, the image is ACCEPTABLE.
If score < {threshold}, mark as NEEDS_IMPROVEMENT with specific suggestions."""

        messages: List[Dict[str, Any]] = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": review_prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                ],
            }
        ]

        try:
            response: Dict[str, Any] = self._make_request(
                model=self.review_model, messages=messages
            )

            choices: List[Dict[str, Any]] = response.get("choices", [])
            if not choices:
                return "Image generated successfully", 7.0, False

            message: Dict[str, Any] = choices[0].get("message", {})
            content: Any = message.get("content", "")

            reasoning: str = message.get("reasoning", "")
            if reasoning and not content:
                content = reasoning

            if isinstance(content, list):
                text_parts: List[str] = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                content = "\n".join(text_parts)

            # Extract score
            score: float = 7.0
            import re

            score_match = re.search(r"SCORE:\s*(\d+(?:\.\d+)?)", content, re.IGNORECASE)
            if score_match:
                score = float(score_match.group(1))
            else:
                score_match = re.search(
                    r"(?:score|rating|quality)[:\s]+(\d+(?:\.\d+)?)",
                    content,
                    re.IGNORECASE,
                )
                if score_match:
                    score = float(score_match.group(1))

            needs_improvement: bool = False
            if "NEEDS_IMPROVEMENT" in content.upper():
                needs_improvement = True
            elif score < threshold:
                needs_improvement = True

            self._log(
                f"✓ Review complete (Score: {score}/10, Threshold: {threshold}/10)"
            )

            return (
                content if content else "Image generated successfully",
                score,
                needs_improvement,
            )
        except Exception as e:
            self._log(f"Review skipped: {str(e)}")
            return "Image generated successfully (review skipped)", 7.0, False

    def improve_prompt(
        self,
        original_prompt: str,
        critique: str,
        iteration: int,
        visual_only: bool = False,
    ) -> str:
        """Improve the generation prompt based on critique.

        Args:
            original_prompt (str): Original user prompt.
            critique (str): Critique from previous iteration.
            iteration (int): Current iteration number.
            visual_only (bool): Whether generating just visual or full slide.

        Returns:
            str: Improved prompt.
        """
        guidelines: str = (
            self.VISUAL_ONLY_GUIDELINES if visual_only else self.FULL_SLIDE_GUIDELINES
        )

        return f"""{guidelines}

USER REQUEST: {original_prompt}

ITERATION {iteration}: Based on previous feedback, address these specific improvements:
{critique}

Generate an improved version that addresses all the critique points."""

    def generate_slide(
        self,
        user_prompt: str,
        output_path: str,
        visual_only: bool = False,
        iterations: int = 2,
        attachments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Generate a slide image or visual with iterative refinement.

        Args:
            user_prompt (str): Description of the slide/visual to generate.
            output_path (str): Path to save final image.
            visual_only (bool): If True, generate just the visual (for PPT workflow).
            iterations (int): Maximum refinement iterations (default: 2).
            attachments (Optional[List[str]]): Optional list of image file paths
                to attach as context.

        Returns:
            Dict[str, Any]: Dictionary with generation results and metadata.
        """
        path_obj: Path = Path(output_path)
        output_dir: Path = path_obj.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        extension: str = path_obj.suffix or ".png"

        mode: str = "visual_only" if visual_only else "full_slide"
        guidelines: str = (
            self.VISUAL_ONLY_GUIDELINES if visual_only else self.FULL_SLIDE_GUIDELINES
        )

        results: Dict[str, Any] = {
            "user_prompt": user_prompt,
            "mode": mode,
            "quality_threshold": self.QUALITY_THRESHOLD,
            "attachments": attachments or [],
            "iterations": [],
            "final_image": None,
            "final_score": 0.0,
            "success": False,
            "early_stop": False,
        }

        current_prompt: str = f"""{guidelines}

USER REQUEST: {user_prompt}

Generate a high-quality {"visual/figure" if visual_only else "presentation slide"} that meets all the guidelines above."""

        print(f"\n{'=' * 60}")
        print(f"Generating Slide {'Visual' if visual_only else 'Image'}")
        print(f"{'=' * 60}")
        print(
            f"Description: {user_prompt[:100]}{'...' if len(user_prompt) > 100 else ''}"
        )
        print(f"Mode: {mode}")
        if attachments:
            print(f"Attachments: {len(attachments)} image(s)")
            for att in attachments:
                print(f"  - {att}")
        print(f"Quality Threshold: {self.QUALITY_THRESHOLD}/10")
        print(f"Max Iterations: {iterations}")
        print(f"Output: {output_path}")
        print(f"{'=' * 60}\n")

        # Track temporary files for cleanup
        temp_files: List[Path] = []
        final_image_data: Optional[bytes] = None

        for i in range(1, iterations + 1):
            print(f"\n[Iteration {i}/{iterations}]")
            print("-" * 40)

            print("Generating image with Nano Banana Pro...")
            image_data: Optional[bytes] = self.generate_image(
                current_prompt, attachments=attachments
            )

            if not image_data:
                error_msg: str = self._last_error or "Image generation failed"
                print(f"✗ Generation failed: {error_msg}")
                results["iterations"].append(
                    {"iteration": i, "success": False, "error": error_msg}
                )
                continue

            # Save to temporary file for review (will be cleaned up)
            import tempfile

            temp_fd, temp_path_str = tempfile.mkstemp(suffix=extension)
            os.close(temp_fd)
            temp_path: Path = Path(temp_path_str)
            temp_files.append(temp_path)

            with open(temp_path, "wb") as f:
                f.write(image_data)
            print(f"✓ Generated image (iteration {i})")

            print("Reviewing image with Gemini 3 Pro...")
            critique, score, needs_improvement = self.review_image(
                str(temp_path), user_prompt, i, visual_only, iterations
            )
            print(f"✓ Score: {score}/10 (threshold: {self.QUALITY_THRESHOLD}/10)")

            results["iterations"].append(
                {
                    "iteration": i,
                    "critique": critique,
                    "score": score,
                    "needs_improvement": needs_improvement,
                    "success": True,
                }
            )

            if not needs_improvement:
                print(
                    f"\n✓ Quality meets threshold ({score} >= {self.QUALITY_THRESHOLD})"
                )
                final_image_data = image_data
                results["final_score"] = score
                results["success"] = True
                results["early_stop"] = True
                break

            if i == iterations:
                print("\n⚠ Maximum iterations reached")
                final_image_data = image_data
                results["final_score"] = score
                results["success"] = True
                break

            print(f"\n⚠ Quality below threshold ({score} < {self.QUALITY_THRESHOLD})")
            print("Improving prompt...")
            current_prompt = self.improve_prompt(
                user_prompt, critique, i + 1, visual_only
            )

        # Clean up temporary files
        for temp_file in temp_files:
            try:
                if temp_file.exists():
                    temp_file.unlink()
            except Exception:
                pass

        # Save only the final image to output path
        if results["success"] and final_image_data:
            with open(output_path, "wb") as f:
                f.write(final_image_data)
            results["final_image"] = str(output_path)
            print(f"\n✓ Final image: {output_path}")

        print(f"\n{'=' * 60}")
        print("Generation Complete!")
        print(f"Final Score: {results['final_score']}/10")
        if results["early_stop"]:
            success_count: int = len(
                [r for r in results["iterations"] if r.get("success")]
            )
            print(f"Iterations Used: {success_count}/{iterations} (early stop)")
        print(f"{'=' * 60}\n")

        return results


def main() -> None:
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate presentation slides or visuals using Nano Banana Pro AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a full slide (for PDF workflow)
  python generate_slide_image_ai.py "Title: Machine Learning Basics\\nKey points: supervised learning, neural networks, deep learning" -o slide_01.png
  
  # Generate just a visual/figure (for PPT workflow)
  python generate_slide_image_ai.py "Neural network architecture diagram with input, hidden, and output layers" -o figure.png --visual-only
  
  # With reference images attached (Nano Banana Pro will see these)
  python generate_slide_image_ai.py "Create a slide explaining this chart with key insights" -o slide.png --attach chart.png
  python generate_slide_image_ai.py "Combine these images into a comparison slide" -o compare.png --attach before.png --attach after.png
  
  # With custom iterations
  python generate_slide_image_ai.py "Title slide for AI Conference 2025" -o title.png --iterations 2
  
  # Verbose output
  python generate_slide_image_ai.py "Data flow diagram" -o flow.png -v

Environment:
  OPENROUTER_API_KEY    OpenRouter API key (required)
        """,
    )

    parser.add_argument("prompt", help="Description of the slide or visual to generate")
    parser.add_argument("-o", "--output", required=True, help="Output image path")
    parser.add_argument(
        "--attach",
        action="append",
        dest="attachments",
        metavar="IMAGE",
        help="Attach image file(s) as context for generation (can use multiple times)",
    )
    parser.add_argument(
        "--visual-only",
        action="store_true",
        help="Generate just the visual/figure (for PPT workflow)",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=2,
        help="Maximum refinement iterations (default: 2)",
    )
    parser.add_argument(
        "--api-key", help="OpenRouter API key (or set OPENROUTER_API_KEY)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    api_key: Optional[str] = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        print("\nSet it with:")
        print("  export OPENROUTER_API_KEY='your_api_key'")
        sys.exit(1)

    if args.iterations < 1 or args.iterations > 2:
        print("Error: Iterations must be between 1 and 2")
        sys.exit(1)

    # Validate attachments exist
    if args.attachments:
        for att in args.attachments:
            if not Path(att).exists():
                print(f"Error: Attachment file not found: {att}")
                sys.exit(1)

    try:
        generator = SlideImageGenerator(api_key=api_key, verbose=args.verbose)
        results: Dict[str, Any] = generator.generate_slide(
            user_prompt=args.prompt,
            output_path=args.output,
            visual_only=args.visual_only,
            iterations=args.iterations,
            attachments=args.attachments,
        )

        if results["success"]:
            print(f"\n✓ Success! Image saved to: {args.output}")
            sys.exit(0)
        else:
            print("\n✗ Generation failed. Check review log for details.")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
