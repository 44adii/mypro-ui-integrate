import React, { useState, useRef } from "react";
import { jsPDF } from "jspdf";
import { LogOut, Mic, Send, FileText, StopCircle, RefreshCw, AlertTriangle, ShieldCheck, Gavel, FileCheck } from "lucide-react";
import { useNavigate } from "react-router-dom";
import ReactMarkdown from 'react-markdown';

// --- Components ---

const LoadingSpinner = ({ text }) => (
    <div className="flex flex-col items-center justify-center space-y-4 py-12 animate-in fade-in zoom-in duration-300">
        <div className="relative h-16 w-16">
            <div className="absolute inset-0 rounded-full border-4 border-gray-700"></div>
            <div className="absolute inset-0 rounded-full border-4 border-t-indigo-500 animate-spin"></div>
        </div>
        <p className="text-gray-400 animate-pulse font-medium">{text}</p>
    </div>
);

const AdvisoryCard = ({ title, value, icon: Icon, colorClass, bgClass }) => (
    <div className={`p-4 rounded-xl border ${bgClass} border-opacity-20 flex items-center space-x-4 shadow-lg transform hover:scale-105 transition duration-200`}>
        <div className={`p-3 rounded-full ${colorClass} bg-opacity-20`}>
            <Icon className={`w-6 h-6 ${colorClass.replace("bg-", "text-")}`} />
        </div>
        <div>
            <p className="text-xs text-gray-400 uppercase tracking-widest font-semibold">{title}</p>
            <p className="text-lg font-bold text-white">{value}</p>
        </div>
    </div>
);

// --- Main Dashboard ---

export default function Dashboard() {
    const navigate = useNavigate();

    // State
    const [input, setInput] = useState("");
    const [isRecording, setIsRecording] = useState(false);
    const [loading, setLoading] = useState(false);
    const [loadingText, setLoadingText] = useState("");
    const [stage, setStage] = useState("input"); // input, analyzed, drafted

    // Data State
    const [advisory, setAdvisory] = useState(null);
    const [caseSummary, setCaseSummary] = useState("");
    const [finalDoc, setFinalDoc] = useState("");
    const [error, setError] = useState("");

    const mediaRecorderRef = useRef(null);
    const chunksRef = useRef([]);

    // --- Auth ---
    const handleLogout = () => {
        localStorage.removeItem("user_token");
        navigate("/");
    };

    const handleReset = () => {
        setStage("input");
        setInput("");
        setAdvisory(null);
        setCaseSummary("");
        setFinalDoc("");
        setError("");
    };

    // --- Voice Logic ---
    // --- Voice Logic (File Upload) ---
    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream, { mimeType: 'audio/webm' });
            chunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (e) => {
                if (e.data.size > 0) chunksRef.current.push(e.data);
            };

            mediaRecorderRef.current.onstop = handleStopRecording;
            mediaRecorderRef.current.start();
            setIsRecording(true);
        } catch (err) {
            console.error("Mic Error:", err);
            setError("Microphone access denied. Please check permissions.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        }
    };

    const handleStopRecording = async () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("file", blob, "recording.webm");

        setLoading(true);
        setLoadingText("Transcribing audio (Local Model)...");

        try {
            const res = await fetch("http://localhost:8001/transcribe", {
                method: "POST",
                body: formData,
            });

            if (!res.ok) throw new Error("Transcription server error.");

            const data = await res.json();
            setInput((prev) => (prev ? prev + " " + data.text : data.text));
        } catch (err) {
            setError(err.message || "Failed to transcribe. Backend might be overloaded.");
        } finally {
            setLoading(false);
        }
    };

    // --- API Calls ---

    const handleAnalyze = async () => {
        if (!input.trim()) return;
        setLoading(true);
        setLoadingText("Thinking... (Analyzing Legal Strategy)");
        setError("");

        try {
            const res = await fetch("http://localhost:8001/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_input: input }),
            });

            if (!res.ok) throw new Error("Analysis failed");

            const data = await res.json();
            // Parse the JSON string from the backend
            const advisoryData = JSON.parse(data.advisory_json);

            setAdvisory(advisoryData);
            setCaseSummary(data.case_summary);
            setStage("analyzed");
        } catch (err) {
            console.error(err);
            let errorMessage = err.message;
            if (errorMessage.includes("Failed to fetch")) {
                errorMessage = "Cannot connect to Backend Server. Please ensure 'uvicorn' is running on port 8001.";
            }
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const handleDraft = async () => {
        setLoading(true);
        setLoadingText("Drafting Legal Document... (Researching IPC & Precedents)");

        try {
            const res = await fetch("http://localhost:8001/draft", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    case_summary: caseSummary,
                    advisory_analysis: JSON.stringify(advisory)
                }),
            });

            if (!res.ok) throw new Error("Drafting failed");

            const data = await res.json();
            setFinalDoc(data.document);
            setStage("drafted");
        } catch (err) {
            setError("Drafting failed. " + err.message);
        } finally {
            setLoading(false);
        }
    };

    // --- Document Handlers ---
    const handleDownloadPDF = () => {
        const doc = new jsPDF();
        const splitText = doc.splitTextToSize(finalDoc, 180);
        doc.setFont("times", "normal");
        doc.setFontSize(12);
        doc.text(splitText, 15, 20);
        doc.save("Legal_Draft_NyayaGPT.pdf");
    };

    const handleEmail = () => {
        alert("Draft sent to lawyer (demo-lawyer@legal.in) successfully!");
    };

    // --- Render Helpers ---

    // Stage 1: Input
    const renderInputStage = () => (
        <div className="w-full max-w-3xl animate-in slide-in-from-bottom-5 duration-500">
            <div className="text-center mb-8">
                <h2 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-400 mb-4">
                    How can I help you today?
                </h2>
                <p className="text-gray-400 text-lg">
                    Describe your situation. I'll analyze if it's civil or criminal, check severity, and guide you.
                </p>
            </div>

            <div className="bg-gray-800 rounded-2xl shadow-2xl overflow-hidden border border-gray-700 focus-within:ring-2 focus-within:ring-indigo-500 transition-all">
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="e.g., My neighbor is playing loud music at night and threatening me..."
                    className="w-full h-40 bg-gray-900/50 p-6 text-lg text-gray-200 placeholder-gray-500 focus:outline-none resize-none"
                />

                <div className="bg-gray-800 p-4 flex items-center justify-between border-t border-gray-700">
                    <div className="flex items-center space-x-4">
                        <button
                            onClick={isRecording ? stopRecording : startRecording}
                            className={`flex items-center gap-2 px-4 py-2 rounded-full font-semibold transition-all shadow-lg ${isRecording
                                ? "bg-red-500/20 text-red-400 hover:bg-red-500/30 animate-pulse border border-red-500/50"
                                : "bg-gray-700 text-gray-300 hover:bg-gray-600 border border-gray-600"
                                }`}
                        >
                            {isRecording ? <StopCircle className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                            {isRecording ? "Listening..." : "Voice Input"}
                        </button>
                    </div>

                    <button
                        onClick={handleAnalyze}
                        disabled={!input.trim()}
                        className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-full font-bold shadow-lg shadow-indigo-500/25 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Analyze <Send className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {error && (
                <div className="mt-4 p-4 rounded-lg bg-red-900/20 border border-red-500/50 text-red-200 flex items-center gap-2 animate-pulse">
                    <AlertTriangle className="w-5 h-5" /> {error}
                </div>
            )}
        </div>
    );

    // Stage 2: Advisory Result
    const renderAdvisoryStage = () => (
        <div className="w-full max-w-4xl animate-in slide-in-from-bottom-10 fade-in duration-500">
            <div className="mb-8 flex items-center justify-center">
                <div className="bg-green-500/10 text-green-400 px-4 py-1.5 rounded-full border border-green-500/20 text-sm font-medium flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4" /> Initial Assessment Complete
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <AdvisoryCard
                    title="Severity"
                    value={advisory?.severity}
                    icon={AlertTriangle}
                    bgClass="bg-orange-500"
                    colorClass="bg-orange-500 text-orange-200"
                />
                <AdvisoryCard
                    title="Legal Type"
                    value={advisory?.legal_type}
                    icon={Gavel}
                    bgClass="bg-blue-500"
                    colorClass="bg-blue-500 text-blue-200"
                />
                <AdvisoryCard
                    title="Best Action"
                    value={advisory?.recommended_action}
                    icon={FileCheck}
                    bgClass="bg-indigo-500"
                    colorClass="bg-indigo-500 text-indigo-200"
                />
            </div>

            <div className="bg-gray-800 rounded-xl p-8 border border-gray-700 shadow-2xl mb-8">
                <h3 className="text-xl font-bold text-gray-200 mb-4 border-b border-gray-700 pb-2">Strategic Guidance</h3>
                <div className="text-gray-300 text-lg leading-relaxed prose prose-invert max-w-none">
                    <ReactMarkdown>{advisory?.step_guidance}</ReactMarkdown>
                </div>
            </div>

            <div className="flex flex-col md:flex-row gap-4 justify-center">
                <button
                    onClick={handleReset}
                    className="px-6 py-3 rounded-xl border border-gray-600 text-gray-300 hover:bg-gray-800 transition font-medium text-sm md:text-base"
                >
                    Try Another Case
                </button>
                <button
                    onClick={handleDraft}
                    className="flex items-center justify-center gap-2 px-8 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 hover:scale-105 transition-all"
                >
                    <FileText className="w-5 h-5" /> Generate {advisory?.recommended_action}
                </button>
            </div>
        </div>
    );

    // Stage 3: Final Document
    const renderFinalStage = () => (
        <div className="w-full max-w-4xl animate-in zoom-in-95 duration-500">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    <FileCheck className="text-green-400" /> Legal Draft Ready
                </h2>
                <button
                    onClick={handleReset}
                    className="text-gray-400 hover:text-white flex items-center gap-1 text-sm bg-gray-800 px-3 py-1.5 rounded-lg hover:bg-gray-700 transition"
                >
                    <RefreshCw className="w-4 h-4" /> Start Over
                </button>
            </div>

            <div className="bg-white text-gray-900 rounded-xl shadow-2xl p-8 md:p-12 overflow-y-auto max-h-[70vh] prose prose-lg prose-indigo max-w-none">
                {/* React Markdown to render the output nicely */}
                <pre className="whitespace-pre-wrap font-serif text-sm md:text-base leading-relaxed">
                    {finalDoc.replace(/```markdown/g, '').replace(/```/g, '')}
                </pre>
            </div>


            <div className="mt-8 flex justify-center gap-4">
                <button
                    onClick={handleDownloadPDF}
                    className="bg-gray-800 hover:bg-gray-700 text-gray-200 px-6 py-3 rounded-lg font-medium transition border border-gray-700 flex items-center gap-2"
                >
                    <FileText className="w-4 h-4" /> Download PDF
                </button>
                <button
                    onClick={handleEmail}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-medium transition shadow-lg flex items-center gap-2"
                >
                    <Send className="w-4 h-4" /> Email to Lawyer
                </button>
            </div>
        </div>
    );

    return (
        <div className="min-h-screen bg-[#0f172a] text-gray-100 flex flex-col font-sans selection:bg-indigo-500/30">
            {/* Navbar */}
            <nav className="border-b border-gray-800 bg-gray-900/60 backdrop-blur-md px-6 py-4 flex justify-between items-center sticky top-0 z-50">
                <div className="flex items-center gap-2">
                    <div className="h-8 w-8 bg-indigo-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-500/20">
                        <Gavel className="text-white w-5 h-5" />
                    </div>
                    <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">NyayaGPT</h1>
                </div>
                <button
                    onClick={handleLogout}
                    className="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition bg-gray-800/50 hover:bg-gray-800 px-4 py-2 rounded-full"
                >
                    <LogOut className="w-4 h-4" /> Sign Out
                </button>
            </nav>

            {/* Main Content Area - CENTERED */}
            <main className="flex-grow flex flex-col items-center justify-center p-4 md:p-8 relative">
                {/* Background Gradients */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-500/10 rounded-full blur-[100px] -z-10 pointer-events-none"></div>

                {loading ? (
                    <LoadingSpinner text={loadingText} />
                ) : (
                    <>
                        {stage === "input" && renderInputStage()}
                        {stage === "analyzed" && renderAdvisoryStage()}
                        {stage === "drafted" && renderFinalStage()}
                    </>
                )}
            </main>
        </div>
    );
}
