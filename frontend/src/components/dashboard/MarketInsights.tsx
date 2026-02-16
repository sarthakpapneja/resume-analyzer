import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, DollarSign, Activity, Target } from "lucide-react";

interface MarketAnalysis {
    role: string;
    salary_range: string;
    demand_level: string;
    demand_growth: string;
    top_skills: string[];
    avg_tenure: string;
}

interface SuccessPrediction {
    interview_probability: number;
    tips: string[];
}

interface MarketInsightsProps {
    marketAnalysis: MarketAnalysis;
    successPrediction: SuccessPrediction;
}

export function MarketInsights({ marketAnalysis, successPrediction }: MarketInsightsProps) {
    if (!marketAnalysis) return null;

    return (
        <div className="space-y-6">
            {/* Market Data */}
            <Card className="border-0 shadow-lg bg-gradient-to-br from-indigo-900 to-purple-900 text-white ring-1 ring-gray-900/5">
                <CardHeader>
                    <CardTitle className="flex items-center text-white">
                        <TrendingUp className="w-5 h-5 mr-3 text-pink-400" />
                        Market Insights: {marketAnalysis.role}
                    </CardTitle>
                    <CardDescription className="text-gray-300">
                        Real-time market data for your target role.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/10">
                            <div className="flex items-center mb-2 text-pink-300">
                                <DollarSign className="w-5 h-5 mr-2" />
                                <span className="font-semibold">Salary Range</span>
                            </div>
                            <p className="text-3xl font-bold">{marketAnalysis.salary_range}</p>
                        </div>

                        <div className="bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/10">
                            <div className="flex items-center mb-2 text-pink-300">
                                <Activity className="w-5 h-5 mr-2" />
                                <span className="font-semibold">Demand Level</span>
                            </div>
                            <div className="flex items-baseline gap-2">
                                <p className="text-3xl font-bold">{marketAnalysis.demand_level}</p>
                                <span className="text-emerald-400 font-bold">{marketAnalysis.demand_growth}</span>
                            </div>
                        </div>

                        <div className="bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/10">
                            <div className="flex items-center mb-2 text-pink-300">
                                <Target className="w-5 h-5 mr-2" />
                                <span className="font-semibold">Hot Skills</span>
                            </div>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {marketAnalysis.top_skills.map((skill, i) => (
                                    <Badge key={i} className="bg-pink-500 hover:bg-pink-600 text-white border-0">
                                        {skill}
                                    </Badge>
                                ))}
                            </div>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Success Prediction */}
            {successPrediction && (
                <Card className="border-0 shadow-lg bg-white ring-1 ring-gray-100">
                    <CardHeader>
                        <CardTitle className="flex items-center text-slate-800">
                            <Target className="w-5 h-5 mr-3 text-indigo-600" />
                            Application Success Predictor
                        </CardTitle>
                        <CardDescription>
                            AI-calculated probability of getting an interview.
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="flex flex-col md:flex-row items-center gap-8">
                            <div className="flex-shrink-0 text-center">
                                <div className="relative flex items-center justify-center w-32 h-32">
                                    <svg className="w-full h-full transform -rotate-90">
                                        <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="12" fill="transparent" className="text-gray-100" />
                                        <circle
                                            cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="12" fill="transparent"
                                            strokeDasharray={2 * Math.PI * 56}
                                            strokeDashoffset={(2 * Math.PI * 56) - ((successPrediction.interview_probability / 100) * (2 * Math.PI * 56))}
                                            strokeLinecap="round"
                                            className={`${successPrediction.interview_probability >= 70 ? "text-emerald-500" : successPrediction.interview_probability >= 40 ? "text-amber-500" : "text-red-500"} transition-all duration-1000 ease-out`}
                                        />
                                    </svg>
                                    <div className="absolute flex flex-col items-center">
                                        <span className="text-3xl font-bold text-gray-800">{successPrediction.interview_probability}%</span>
                                        <span className="text-xs text-gray-500 font-medium">Likelihood</span>
                                    </div>
                                </div>
                            </div>

                            <div className="flex-grow space-y-3">
                                <h4 className="font-semibold text-gray-700">Improve your odds:</h4>
                                {successPrediction.tips.map((tip, i) => (
                                    <div key={i} className="flex items-start p-3 bg-slate-50 rounded-lg border border-slate-200 shadow-sm">
                                        <TrendingUp className="w-5 h-5 mr-3 text-indigo-500 mt-0.5 flex-shrink-0" />
                                        <p className="text-gray-600 text-sm">{tip}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}
