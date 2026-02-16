"use client";

import { useState } from "react";
import { analyzeResume } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  UploadCloud,
  FileText,
  AlertTriangle,
  Loader2,
  Sparkles,
  ArrowRight,
  LayoutDashboard,
  Layers,
  LineChart,
  Briefcase,
  PenTool,
} from "lucide-react";

// Import Modular Components
import { ScoreOverview } from "@/components/dashboard/ScoreOverview";
import { SkillAnalysis } from "@/components/dashboard/SkillAnalysis";
import { MarketInsights } from "@/components/dashboard/MarketInsights";
import { InterviewPrep } from "@/components/dashboard/InterviewPrep";
import { BulletImprover } from "@/components/dashboard/BulletImprover";

// Types
interface TrajectoryItem {
  skill: string;
  new_score: number;
  boost: number;
}

interface AnalysisResult {
  score: number;
  missing_skills: string[];
  present_skills: string[];
  recommendations: string[];
  trajectory: TrajectoryItem[];
  interview_questions: any[];
  bullet_analysis: any[];
  market_analysis: any;
  success_prediction: any;
  github_analysis: any;
  structure_analysis: any;
  resume_parsing_status: string;
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jdFile, setJdFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleJdFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setJdFile(e.target.files[0]);
      setJobDescription("");
    }
  };

  const handleAnalyze = async () => {
    if (!file || (!jobDescription && !jdFile)) {
      setError("Please upload a resume and provide a job description (Text or File).");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const data = await analyzeResume(file, jobDescription, jdFile, "");
      setResult(data);
    } catch (err: any) {
      setError(err.message || "An error occurred during analysis.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 font-sans">
      {/* Top Navigation / Header */}
      <div className="bg-white border-b sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="bg-indigo-600 p-1.5 rounded-lg">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-xl text-gray-900 tracking-tight">Skill Gap Analyzer</span>
          </div>
          {result && (
            <Button variant="ghost" size="sm" onClick={() => setResult(null)} className="text-gray-500 hover:text-red-600">
              <ArrowRight className="w-4 h-4 mr-1 rotate-180" /> Start New Analysis
            </Button>
          )}
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6 md:p-8 space-y-8">
        {!result ? (
          // Input Form View
          <div className="animate-in fade-in slide-in-from-bottom-8 duration-700">
            <div className="text-center mb-12 space-y-4">
              <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight">
                Optimize your resume for the <span className="text-indigo-600">AI Era</span>.
              </h1>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Get instant feedback, market insights, and tailored improvement suggestions to land your dream job.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              {/* Upload Resume */}
              <Card className="lg:col-span-5 border-0 shadow-xl ring-1 ring-gray-200">
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <FileText className="w-5 h-5 mr-2 text-indigo-600" />
                    Upload Resume
                  </CardTitle>
                  <CardDescription>PDF or DOCX (Max 5MB)</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="group relative border-2 border-dashed border-gray-300 hover:border-indigo-500 rounded-xl p-10 transition-all bg-gray-50/50 hover:bg-white text-center cursor-pointer">
                    <input
                      type="file"
                      accept=".pdf,.docx"
                      onChange={handleFileChange}
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                    />
                    <div className="flex flex-col items-center space-y-3">
                      <div className="p-3 bg-white rounded-full shadow-md group-hover:scale-110 transition-transform ring-1 ring-gray-100">
                        {file ? <FileText className="w-6 h-6 text-indigo-600" /> : <UploadCloud className="w-6 h-6 text-indigo-400" />}
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">{file ? file.name : "Drop resume here"}</p>
                        <p className="text-xs text-gray-500 mt-1">{file ? "Ready to upload" : "or click to browse"}</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Job Description */}
              <Card className="lg:col-span-7 border-0 shadow-xl ring-1 ring-gray-200">
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <Briefcase className="w-5 h-5 mr-2 text-indigo-600" />
                    Job Details
                  </CardTitle>
                  <CardDescription>Paste the job description or upload a file.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <Tabs defaultValue="text" className="w-full">
                    <TabsList className="grid w-full grid-cols-2 mb-4">
                      <TabsTrigger value="text">Paste Text</TabsTrigger>
                      <TabsTrigger value="file">Upload JD File</TabsTrigger>
                    </TabsList>
                    <TabsContent value="text">
                      <Textarea
                        placeholder="Paste job description here..."
                        className="min-h-[150px] resize-none focus-visible:ring-indigo-500"
                        value={jobDescription}
                        onChange={(e) => {
                          setJobDescription(e.target.value);
                          setJdFile(null);
                        }}
                      />
                    </TabsContent>
                    <TabsContent value="file">
                      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center bg-gray-50 relative">
                        <input
                          type="file"
                          accept=".pdf,.docx,.txt"
                          onChange={handleJdFileChange}
                          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                        />
                        <p className="text-sm text-gray-600">
                          {jdFile ? jdFile.name : "Click to upload JD File"}
                        </p>
                      </div>
                    </TabsContent>
                  </Tabs>

                  <Button
                    size="lg"
                    onClick={handleAnalyze}
                    disabled={loading || !file || (!jobDescription && !jdFile)}
                    className="w-full h-12 text-base bg-indigo-600 hover:bg-indigo-700 shadow-lg shadow-indigo-200/50"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Analyzing...
                      </>
                    ) : (
                      "Start Analysis"
                    )}
                  </Button>
                </CardContent>
              </Card>
            </div>

            {error && (
              <Alert variant="destructive" className="mt-8 max-w-3xl mx-auto">
                <AlertTriangle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
          </div>
        ) : (
          // Results Dashboard View with Tabs
          <div className="animate-in fade-in zoom-in-95 duration-500">
            <Tabs defaultValue="dashboard" className="space-y-6">

              {/* Navigation Tabs */}
              <div className="sticky top-20 z-40 bg-slate-50/90 backdrop-blur pb-4">
                <TabsList className="w-full flex justify-between gap-2 overflow-x-auto h-auto p-1 bg-white border shadow-sm rounded-xl">
                  <TabsTrigger value="dashboard" className="flex-1 py-3 data-[state=active]:bg-indigo-50 data-[state=active]:text-indigo-700 data-[state=active]:shadow-none">
                    <LayoutDashboard className="w-4 h-4 mr-2" /> Overview
                  </TabsTrigger>
                  <TabsTrigger value="skills" className="flex-1 py-3 data-[state=active]:bg-indigo-50 data-[state=active]:text-indigo-700 data-[state=active]:shadow-none">
                    <Layers className="w-4 h-4 mr-2" /> Skills
                  </TabsTrigger>
                  <TabsTrigger value="market" className="flex-1 py-3 data-[state=active]:bg-indigo-50 data-[state=active]:text-indigo-700 data-[state=active]:shadow-none">
                    <LineChart className="w-4 h-4 mr-2" /> Market
                  </TabsTrigger>
                  <TabsTrigger value="resume" className="flex-1 py-3 data-[state=active]:bg-indigo-50 data-[state=active]:text-indigo-700 data-[state=active]:shadow-none">
                    <PenTool className="w-4 h-4 mr-2" /> Resume Studio
                  </TabsTrigger>
                  <TabsTrigger value="interview" className="flex-1 py-3 data-[state=active]:bg-indigo-50 data-[state=active]:text-indigo-700 data-[state=active]:shadow-none">
                    <Briefcase className="w-4 h-4 mr-2" /> Interview
                  </TabsTrigger>
                </TabsList>
              </div>

              {/* Tab Content Areas */}

              {/* 1. Dashboard Overview */}
              <TabsContent value="dashboard" className="space-y-6 animate-in slide-in-from-right-4 duration-300">
                <ScoreOverview score={result.score} structureAnalysis={result.structure_analysis} />

                {/* Quick Actions / Key Recommendations */}
                <Card className="border-0 shadow-lg ring-1 ring-gray-100">
                  <CardHeader>
                    <CardTitle>Top Priority Actions</CardTitle>
                    <CardDescription>Critical steps to improve your score immediately.</CardDescription>
                  </CardHeader>
                  <CardContent className="grid gap-4 md:grid-cols-2">
                    {result.recommendations.slice(0, 4).map((rec, i) => (
                      <div key={i} className="flex items-start p-4 bg-orange-50 border border-orange-100 rounded-lg">
                        <div className="bg-orange-100 p-1.5 rounded-full mr-3 text-orange-600 font-bold text-xs">{i + 1}</div>
                        <p className="text-sm text-gray-800">{rec}</p>
                      </div>
                    ))}
                  </CardContent>
                </Card>
              </TabsContent>

              {/* 2. Skills Deep Dive */}
              <TabsContent value="skills" className="animate-in slide-in-from-right-4 duration-300">
                <SkillAnalysis
                  missingSkills={result.missing_skills}
                  presentSkills={result.present_skills}
                  trajectory={result.trajectory}
                  currentScore={result.score}
                />
              </TabsContent>

              {/* 3. Market Insights */}
              <TabsContent value="market" className="animate-in slide-in-from-right-4 duration-300">
                <MarketInsights
                  marketAnalysis={result.market_analysis}
                  successPrediction={result.success_prediction}
                />
              </TabsContent>

              {/* 4. Resume Studio (Bullet Improver) */}
              <TabsContent value="resume" className="animate-in slide-in-from-right-4 duration-300">
                <BulletImprover bullets={result.bullet_analysis} />
              </TabsContent>

              {/* 5. Interview Prep */}
              <TabsContent value="interview" className="animate-in slide-in-from-right-4 duration-300">
                <InterviewPrep questions={result.interview_questions} />
              </TabsContent>

            </Tabs>
          </div>
        )}
      </div>
    </main>
  );
}
