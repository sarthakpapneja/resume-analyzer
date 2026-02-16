import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Briefcase } from "lucide-react";

interface InterviewQuestion {
    category: string;
    skill: string;
    question: string;
    difficulty: string;
}

interface InterviewPrepProps {
    questions: InterviewQuestion[];
}

export function InterviewPrep({ questions }: InterviewPrepProps) {
    if (!questions || questions.length === 0) return null;

    return (
        <Card className="border-0 shadow-lg bg-white ring-1 ring-gray-100">
            <CardHeader>
                <CardTitle className="flex items-center">
                    <Briefcase className="w-5 h-5 mr-3 text-indigo-600" />
                    Mock Interview Prep
                </CardTitle>
                <CardDescription>
                    AI-generated questions targeting your specific skill gaps and strengths.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
                    {questions.map((q, i) => (
                        <div key={i} className="group p-5 rounded-xl border border-gray-100 hover:border-indigo-100 hover:shadow-md transition-all bg-gray-50/50 hover:bg-white">
                            <div className="flex justify-between items-start mb-3">
                                <div className="flex gap-2 items-center">
                                    <Badge variant="outline" className={`${q.category.includes("Weakness") ? "text-amber-600 bg-amber-50 border-amber-200" : "text-emerald-600 bg-emerald-50 border-emerald-200"}`}>
                                        {q.category}
                                    </Badge>
                                    <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">{q.skill}</span>
                                </div>
                                <span className="text-xs text-gray-400 font-medium px-2 py-1 bg-gray-100 rounded-full">{q.difficulty}</span>
                            </div>
                            <p className="text-gray-800 font-medium text-lg mt-1 group-hover:text-indigo-700 transition-colors leading-relaxed">
                                {q.question}
                            </p>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}
