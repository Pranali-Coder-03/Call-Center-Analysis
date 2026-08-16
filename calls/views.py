import os
import tempfile

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages

from .models import CallRecording
from .gemini_service import analyze_audio
from .storage_service import (
    upload_recording,
    get_public_url,
    delete_recording_file
)
from .pdf_report import create_pdf


# ============================================================
# DASHBOARD
# ============================================================

def dashboard(request):

    return render(
        request,
        "calls/dashboard.html"
    )


# ============================================================
# ANALYZE CALL
# ============================================================

def analyze_call(request):

    if request.method == "POST":

        # ----------------------------------------------------
        # Get uploaded file
        # ----------------------------------------------------

        audio_file = request.FILES.get("recording")

        if not audio_file:

            return render(
                request,
                "calls/analyze_call.html",
                {
                    "error": "Please select a call recording."
                }
            )

        # ----------------------------------------------------
        # Allowed extensions
        # ----------------------------------------------------

        allowed_extensions = [
            ".mp4",
            ".mp3",
            ".wav",
            ".ogg",
            ".aac",
            ".flac",
            ".m4a",
        ]

        file_extension = os.path.splitext(
            audio_file.name
        )[1].lower()

        if file_extension not in allowed_extensions:

            return render(
                request,
                "calls/analyze_call.html",
                {
                    "error": (
                        "Unsupported file format. "
                        "Please upload MP4, MP3, WAV, OGG, "
                        "AAC, FLAC, or M4A."
                    )
                }
            )

        # ----------------------------------------------------
        # File size validation
        # ----------------------------------------------------

        max_size = 50 * 1024 * 1024

        if audio_file.size > max_size:

            return render(
                request,
                "calls/analyze_call.html",
                {
                    "error": "Maximum file size is 50 MB."
                }
            )

        # ----------------------------------------------------
        # Create database record
        # ----------------------------------------------------

        call = CallRecording.objects.create(
            file_name=audio_file.name,
            status="analyzing"
        )

        temp_path = None

        try:

            # =================================================
            # STEP 1
            # Save uploaded file temporarily
            # =================================================

            suffix = file_extension

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:

                for chunk in audio_file.chunks():

                    temp_file.write(chunk)

                temp_path = temp_file.name

            # =================================================
            # STEP 2
            # VERY IMPORTANT
            # Reset uploaded file pointer
            # =================================================

            # Upload original file to Supabase

            audio_file.seek(0)

            storage_name = upload_recording(
                audio_file
            )

            file_url = get_public_url(
                storage_name
            )

            call.storage_path = storage_name
            call.file_url = file_url

            call.save(
                update_fields=[
                    "storage_path",
                    "file_url"
                ]
            )

            # =================================================
            # STEP 6
            # Analyze audio with Gemini
            # =================================================

            result = analyze_audio(
                temp_path
            )

            # =================================================
            # STEP 7
            # Save AI analysis
            # =================================================

            call.summary = result.get(
                "summary",
                ""
            )

            call.customer_issue = result.get(
                "customer_issue",
                ""
            )

            call.resolution = result.get(
                "resolution",
                ""
            )

            call.sentiment = result.get(
                "sentiment",
                ""
            )

            call.agent_performance = result.get(
                "agent_performance",
                ""
            )

            # ------------------------------------------------
            # Key topics
            # ------------------------------------------------

            key_topics = result.get(
                "key_topics",
                []
            )

            if isinstance(key_topics, list):

                call.key_topics = ", ".join(
                    str(item)
                    for item in key_topics
                )

            else:

                call.key_topics = str(
                    key_topics
                )

            # ------------------------------------------------
            # Action items
            # ------------------------------------------------

            action_items = result.get(
                "action_items",
                []
            )

            if isinstance(action_items, list):

                call.action_items = ", ".join(
                    str(item)
                    for item in action_items
                )

            else:

                call.action_items = str(
                    action_items
                )

            # =================================================
            # STEP 8
            # Mark analysis completed
            # =================================================

            call.status = "completed"

            call.analyzed_at = timezone.now()

            call.save()

            # =================================================
            # STEP 9
            # Show result
            # =================================================

            return redirect(
                "analyze_call_result",
                call_id=call.id
            )

        except Exception as e:

            # =================================================
            # Something failed
            # =================================================

            call.status = "failed"

            call.save(
                update_fields=[
                    "status"
                ]
            )

            return render(
                request,
                "calls/analyze_call.html",
                {
                    "error": (
                        f"Analysis failed: {str(e)}"
                    )
                }
            )

        finally:

            # =================================================
            # Delete temporary file
            # =================================================

            if (
                temp_path
                and os.path.exists(temp_path)
            ):

                try:

                    os.remove(
                        temp_path
                    )

                except OSError:

                    pass

    # ========================================================
    # GET request
    # ========================================================

    return render(
        request,
        "calls/analyze_call.html"
    )


# ============================================================
# ANALYSIS RESULT
# ============================================================

def analyze_call_result(
    request,
    call_id
):

    call = get_object_or_404(
        CallRecording,
        id=call_id
    )

    return render(
        request,
        "calls/analyze_call.html",
        {
            "call": call
        }
    )


# ============================================================
# VIEW ALL RECORDINGS
# ============================================================

def view_recordings(request):

    calls = (
        CallRecording.objects
        .all()
        .order_by("-created_at")
    )

    return render(
        request,
        "calls/recordings.html",
        {
            "calls": calls
        }
    )


# ============================================================
# DOWNLOAD PDF REPORT
# ============================================================

def download_report(
    request,
    call_id
):

    call = get_object_or_404(
        CallRecording,
        id=call_id
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        f'attachment; '
        f'filename="call_report_{call.id}.pdf"'
    )

    create_pdf(
        call,
        response
    )

    return response


# ============================================================
# DELETE RECORDING
# ============================================================

def delete_recording(request, call_id):

    if request.method != "POST":
        return redirect("recordings")

    call = get_object_or_404(
        CallRecording,
        id=call_id
    )

    try:

        # Delete file from Supabase Storage
        if call.storage_path:

            print("Deleting Supabase file:")
            print(call.storage_path)

            delete_recording_file(
                call.storage_path
            )

        # Delete Django database record
        call.delete()

        messages.success(
            request,
            "Call recording deleted successfully."
        )

    except Exception as e:

        print("DELETE ERROR:", str(e))

        messages.error(
            request,
            f"Unable to delete recording: {str(e)}"
        )

    return redirect("recordings")