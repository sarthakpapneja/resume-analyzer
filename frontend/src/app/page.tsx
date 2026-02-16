"use client";

import { useState } from "react";
import { analyzeResume } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { UploadCloud, FileText, CheckCircle, AlertTriangle, Loader2 } from "lucide-react";

interface AnalysisResult {
  score: number;
  missing_skills: string[];
  recommendations: string[];
  resume_parsing_status: string;
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!file || !jobDescription) {
      setError("Please upload a resume and provide a job description.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const data = await analyzeResume(file, jobDescription);
      setResult(data);
    } catch (err: any) {
      setError(err.message || "An error occurred during analysis.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-5xl mx-auto space-y-8">
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-gray-900">Resume Analyzer</h1>
            <p className="text-gray-500 mt-2">AI-powered Match Scoring & Skill Gap Detection</p>
          </div>
        </header>

        {!result ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Upload Section */}
            <Card>
              <CardHeader>
                <CardTitle>1. Upload Resume</CardTitle>
                <CardDescription>PDF or DOCX format</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="border-2 border-dashed border-gray-200 rounded-lg p-10 flex flex-col items-center justify-center space-y-4 hover:bg-gray-50 transition-colors cursor-pointer relative">
                  <input
                    type="file"
                    accept=".pdf,.docx"
                    onChange={handleFileChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                  <div className="p-4 bg-indigo-50 rounded-full text-indigo-600">
                    {file ? <FileText className="w-8 h-8" /> : <UploadCloud className="w-8 h-8" />}
                  </div>
                  <div className="text-center">
                    <p className="text-sm font-medium text-gray-900">
                      {file ? file.name : "Click to upload or drag and drop"}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {file ? `${(file.size / 1024).toFixed(1)} KB` : "PDF, DOCX up to 5MB"}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* JD Input Section */}
            <Card>
              <CardHeader>
                <CardTitle>2. Job Description</CardTitle>
                <CardDescription>Paste the job requirements here</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  placeholder="Paste job description..."
                  className="min-h-[200px]"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                />
              </CardContent>
            </Card>

            <div className="md:col-span-2 flex justify-end">
              <Button
                size="lg"
                onClick={handleAnalyze}
                disabled={loading || !file || !jobDescription}
                className="w-full md:w-auto"
              >
                {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Analyze Match
              </Button>
            </div>

            {error && (
              <div className="md:col-span-2">
                <Alert variant="destructive">
                  <AlertTriangle className="h-4 w-4" />
                  <AlertTitle>Error</AlertTitle>
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center justify-between">
              <Button variant="outline" onClick={() => setResult(null)}>
                ← Analyze Another
              </Button>
            </div>

            {/* Score Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="col-span-1 border-indigo-100 shadow-md">
                <CardHeader>
                  <CardTitle>Match Score</CardTitle>
                </CardHeader>
                <CardContent className="flex flex-col items-center justify-center py-6">
                  <div className="relative flex items-center justify-center">
                    <svg className="w-40 h-40 transform -rotate-90">
                      <circle
                        cx="80"
                        cy="80"
                        r="70"
                        stroke="currentColor"
                        strokeWidth="10"
                        fill="transparent"
                        className="text-gray-200"
                      />
                      <circle
                        cx="80"
                        cy="80"
                        r="70"
                        stroke="currentColor"
                        strokeWidth="10"
                        fill="transparent"
                        strokeDasharray={440}
                        strokeDashoffset={440 - (440 * result.score) / 100}
                        className={`text-indigo-600 transition-all duration-1000 ease-out`}
                      />
                    </svg>
                    <span className="absolute text-4xl font-bold text-gray-900">{result.score}%</span>
                  </div>
                  <p className="mt-4 text-sm font-medium text-gray-500">
                    {result.score > 75 ? "Excellent Match" : result.score > 50 ? "Moderate Match" : "Low Match"}
                  </p>
                </CardContent>
              </Card>

              {/* Missing Skills */}
              <Card className="col-span-1 md:col-span-2">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <AlertTriangle className="w-5 h-5 text-amber-500" />
                    Missing Skills
                  </CardTitle>
                  <CardDescription>
                    Skills found in the job description but not in your resume.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {result.missing_skills.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                      {result.missing_skills.map((skill) => (
                        <span key={skill} className="px-3 py-1 bg-red-50 text-red-700 rounded-full text-sm font-medium border border-red-100">
                          {skill}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 text-green-600">
                      <CheckCircle className="w-5 h-5" />
                      <span>No major skills missing!</span>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Recommendations */}
            <Card>
              <CardHeader>
                <CardTitle>AI Recommendations</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {result.recommendations.map((rec, i) => (
                    <li key={i} className="flex gap-3 text-gray-700 p-3 bg-gray-50 rounded-lg">
                      <div className="min-w-6 h-6 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 text-xs font-bold mt-0.5">
                        {i + 1}
                      </div>
                      <span className="text-sm">{rec}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </main>
  );
}
