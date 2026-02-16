import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles, CheckCircle2, XCircle, AlertCircle } from "lucide-react";

interface BulletAnalysis {
    text: string;
    score: number;
    suggestions: string[];
}

interface BulletImproverProps {
    bullets: BulletAnalysis[];
}

export function BulletImprover({ bullets }: BulletImproverProps) {
    const [selectedBulletIndex, setSelectedBulletIndex] = useState(0);

    if (!bullets || bullets.length === 0) {
        return (
            <Card className="border-0 shadow-sm bg-slate-50">
                <CardContent className="py-12 text-center text-gray-500">
                    <CheckCircle2 className="w-12 h-12 mx-auto mb-3 text-emerald-500" />
                    <p>No weak bullet points detected! Your resume is looking strong.</p>
                </CardContent>
            </Card>
        );
    }

    const selectedBullet = bullets[selectedBulletIndex];

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[600px]">
            {/* Left Panel: List of Bullets */}
            <Card className="col-span-1 border-0 shadow-lg ring-1 ring-gray-100 flex flex-col h-full bg-white">
                <CardHeader className="pb-3 border-b">
                    <CardTitle className="text-lg flex items-center">
                        <AlertCircle className="w-5 h-5 mr-2 text-amber-500" />
                        Needs Improvement
                    </CardTitle>
                    <CardDescription>Select a point to analyze</CardDescription>
                </CardHeader>
                <CardContent className="p-0 flex-grow overflow-y-auto custom-scrollbar">
                    <div className="divide-y">
                        {bullets.map((bullet, i) => (
                            <div
                                key={i}
                                onClick={() => setSelectedBulletIndex(i)}
                                className={`p-4 cursor-pointer transition-all hover:bg-slate-50 ${selectedBulletIndex === i ? "bg-indigo-50 border-l-4 border-indigo-500" : "border-l-4 border-transparent"
                                    }`}
                            >
                                <p className="text-sm text-gray-700 line-clamp-2 italic">"{bullet.text}"</p>
                                <div className="flex items-center justify-between mt-2">
                                    <Badge variant={bullet.score < 50 ? "destructive" : "secondary"} className="text-xs">
                                        Score: {bullet.score}/100
                                    </Badge>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Right Panel: Analysis Detail */}
            <Card className="col-span-1 lg:col-span-2 border-0 shadow-xl ring-1 ring-gray-100 h-full flex flex-col bg-slate-50/50">
                <CardHeader className="bg-white border-b">
                    <div className="flex justify-between items-start">
                        <div>
                            <CardTitle className="text-indigo-700">Analysis & Fixes</CardTitle>
                            <CardDescription>AI-powered suggestions for impact.</CardDescription>
                        </div>
                        <div className="flex items-center space-x-2">
                            <span className="text-sm text-gray-500">Impact Score</span>
                            <span className={`text-2xl font-bold ${selectedBullet.score < 50 ? 'text-red-500' : 'text-amber-500'}`}>
                                {selectedBullet.score}
                            </span>
                        </div>
                    </div>
                </CardHeader>
                <CardContent className="p-6 overflow-y-auto">
                    <div className="mb-6">
                        <h4 className="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2">Original Text</h4>
                        <div className="p-4 bg-white border border-gray-200 rounded-lg text-gray-800 italic relative">
                            <span className="absolute top-2 left-2 text-4xl text-gray-100 font-serif">"</span>
                            <p className="relative z-10 pl-4">{selectedBullet.text}</p>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <h4 className="text-xs font-semibold uppercase tracking-wider text-gray-500">Action Items</h4>
                        {selectedBullet.suggestions.map((suggestion, i) => (
                            <div key={i} className="flex items-start p-4 bg-white border border-indigo-100 rounded-xl shadow-sm">
                                <div className="bg-indigo-100 p-2 rounded-full mr-4 flex-shrink-0">
                                    <Sparkles className="w-4 h-4 text-indigo-600" />
                                </div>
                                <div>
                                    <p className="text-gray-700 font-medium">{suggestion}</p>
                                    {/* Heuristic contextual help based on suggestion content */}
                                    {suggestion.includes("strong action verb") && (
                                        <p className="text-xs text-slate-500 mt-1">Try verbs like: <strong>Spearheaded, Orchestrated, Engineered, Revitalized</strong>.</p>
                                    )}
                                    {suggestion.includes("quantification") && (
                                        <p className="text-xs text-slate-500 mt-1">Ask yourself: "How many?", "How much?", "How fast?". Use <strong>%</strong>, <strong>$</strong>, or <strong>numbers</strong>.</p>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Simulated "After" Example (Simple heuristic for now, ideal for Generative AI step later) */}
                    <div className="mt-8 p-4 bg-emerald-50 border border-emerald-100 rounded-lg">
                        <h4 className="text-sm font-semibold text-emerald-800 flex items-center mb-2">
                            <CheckCircle2 className="w-4 h-4 mr-2" />
                            Pro Tip
                        </h4>
                        <p className="text-sm text-emerald-700">
                            Structure your bullet as: <strong>Action Verb</strong> + <strong>Task/Project</strong> + <strong>Result/Impact (Metrics)</strong>.
                        </p>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
