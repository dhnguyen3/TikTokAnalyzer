import gradio as gr
from analyzer.core import TikTokAnalyzer
from analyzer.utils import save_uploaded_file, cleanup_temp_files

analyzer = TikTokAnalyzer()

def analyze_video(tiktok_video, reference_video):
    try:
        # Save uploaded files
        tiktok_path = save_uploaded_file(tiktok_video)
        ref_path = save_uploaded_file(reference_video)
        
        # Run analysis
        result = analyzer.analyze(tiktok_path, ref_path)
        
        # Format output
        feedback = "\n".join(result.feedback) if result.feedback else "✅ All checks passed"
        
        return {
            "score": result.score,
            "brightness": f"{result.visual_metrics['brightness']:.1f}",
            "contrast": f"{result.visual_metrics['contrast']:.1f}",
            "product": "✅ Visible" if result.visual_metrics['product_visible'] else "❌ Not found",
            "brand_mentions": ", ".join(result.brand_consistency['mentions']) or "None",
            "feedback": feedback
        }
    finally:
        # Cleanup
        cleanup_temp_files(tiktok_path)
        cleanup_temp_files(ref_path)

# Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🎵 TikTok Quality Analyzer")
    
    with gr.Row():
        with gr.Column():
            video_input = gr.File(label="Upload TikTok Video", file_types=["video"])
            reference_input = gr.File(label="Reference Video", file_types=["video"])
            analyze_btn = gr.Button("Analyze", variant="primary")
        
        with gr.Column():
            score_output = gr.Label(label="Quality Score")
            brightness_out = gr.Textbox(label="Brightness (0-255)")
            contrast_out = gr.Textbox(label="Contrast")
            product_out = gr.Textbox(label="Product Visibility")
            brand_out = gr.Textbox(label="Brand Mentions")
            feedback_out = gr.Textbox(label="Feedback", lines=3)
    
    analyze_btn.click(
        fn=analyze_video,
        inputs=[video_input, reference_input],
        outputs=[score_output, brightness_out, contrast_out, product_out, brand_out, feedback_out]
    )

if __name__ == "__main__":
    app.launch()