import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { FileText, CheckCircle2, AlertTriangle } from "lucide-react";

interface StructureAnalysis {
    file_size_kb: number;
    text_length: number;
    is_scanned_pdf: boolean;
    contact_info_present: boolean;
}

interface ScoreOverviewProps {
    score: number;
    structureAnalysis: StructureAnalysis;
}

const CircularProgress = ({ score }: { score: number }) => {
    const radius = 60;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (score / 100) * circumference;

    const getColor = (s: number) => {
        if (s >= 80) return "text-emerald-500";
        if (s >= 50) return "text-amber-500";
        return "text-red-500";
    };

    return (
        <div className="relative flex items-center justify-center w-40 h-40">
            <svg className="w-full h-full transform -rotate-90">
                <circle cx="80" cy="80" r={radius} stroke="currentColor" strokeWidth="8" fill="transparent" className="text-gray-100" />
                <circle
                    cx="80" cy="80" r={radius} stroke="currentColor" strokeWidth="8" fill="transparent"
                    strokeDasharray={circumference}
                    strokeDashoffset={strokeDashoffset}
                    strokeLinecap="round"
                    className={`${getColor(score)} transition-all duration-1000 ease-out`}
                />
            </svg>
            <div className="absolute flex flex-col items-center">
                <span className={`text-3xl font-bold ${getColor(score)}`}>{Math.round(score)}%</span>
                <span className="text-xs text-gray-400 font-medium uppercase tracking-wide">Match</span>
            </div>
        </div>
    );
};

export function ScoreOverview({ score, structureAnalysis }: ScoreOverviewProps) {
    const getScoreLabel = (score: number) => {
        if (score >= 75) return "Excellent Match";
        if (score >= 50) return "Good Potential";
        return "Needs Improvement";
    };

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Score Card */}
            <Card className="border-0 shadow-lg bg-white ring-1 ring-gray-100">
                <CardHeader>
                    <CardTitle>Resume Match Score</CardTitle>
                    <CardDescription>Overall alignment with the job description.</CardDescription>
                </CardHeader>
                <CardContent className="flex flex-col items-center justify-center py-6">
                    <CircularProgress score={score} />
                    <Badge variant={score > 75 ? "default" : score > 50 ? "secondary" : "destructive"} className="mt-4 text-sm px-4 py-1">
                        {getScoreLabel(score)}
                    </Badge>
                </CardContent>
            </Card>

            {/* ATS Health Check */}
            <Card className="border-0 shadow-lg bg-slate-900 text-white ring-1 ring-gray-900/5">
                <CardHeader>
                    <CardTitle className="flex items-center text-white">
                        <FileText className="w-5 h-5 mr-3 text-indigo-400" />
                        ATS Compatibility
                    </CardTitle>
                    <CardDescription className="text-slate-400">Technical health check.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg border border-white/10">
                        <span className="text-slate-300">File Size</span>
                        <span className="font-mono font-bold">{Math.round(structureAnalysis.file_size_kb)} KB</span>
                    </div>

                    <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg border border-white/10">
                        <span className="text-slate-300">Parsable Text</span>
                        <div className="flex items-center">
                            {structureAnalysis.text_length < 200 ?
                                <span className="text-red-400 text-sm flex items-center"><AlertTriangle className="w-3 h-3 mr-1" /> Too Short</span> :
                                <span className="text-emerald-400 text-sm flex items-center"><CheckCircle2 className="w-3 h-3 mr-1" /> Good</span>
                            }
                        </div>
                    </div>

                    <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg border border-white/10">
                        <span className="text-slate-300">Contact Info</span>
                        <div className="flex items-center">
                            {structureAnalysis.contact_info_present ?
                                <span className="text-emerald-400 text-sm flex items-center"><CheckCircle2 className="w-3 h-3 mr-1" /> Found</span> :
                                <span className="text-amber-400 text-sm flex items-center"><AlertTriangle className="w-3 h-3 mr-1" /> Missing</span>
                            }
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
