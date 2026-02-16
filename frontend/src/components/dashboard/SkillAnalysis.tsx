import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertTriangle, CheckCircle2, Sparkles } from "lucide-react";

interface TrajectoryItem {
    skill: string;
    new_score: number;
    boost: number;
}

interface SkillAnalysisProps {
    missingSkills: string[];
    presentSkills: string[];
    trajectory: TrajectoryItem[];
    currentScore: number;
}

export function SkillAnalysis({ missingSkills, presentSkills, trajectory, currentScore }: SkillAnalysisProps) {
    const [showAllMissing, setShowAllMissing] = useState(false);

    return (
        <div className="space-y-6">
            {/* Skills Tabs */}
            <Card className="border-0 shadow-lg ring-1 ring-gray-100 min-h-[400px]">
                <CardHeader>
                    <CardTitle>Skill Gap Analysis</CardTitle>
                    <CardDescription>Compare your skills against the job requirements.</CardDescription>
                </CardHeader>
                <CardContent>
                    <Tabs defaultValue="missing" className="w-full">
                        <TabsList className="mb-6 w-full justify-start bg-gray-100/50 p-1">
                            <TabsTrigger value="missing" className="flex-1 data-[state=active]:bg-white data-[state=active]:shadow-sm">
                                <AlertTriangle className="w-4 h-4 mr-2 text-amber-500" />
                                Missing Skills ({missingSkills.length})
                            </TabsTrigger>
                            <TabsTrigger value="present" className="flex-1 data-[state=active]:bg-white data-[state=active]:shadow-sm">
                                <CheckCircle2 className="w-4 h-4 mr-2 text-emerald-500" />
                                Matched Skills ({presentSkills.length})
                            </TabsTrigger>
                        </TabsList>

                        <TabsContent value="missing" className="space-y-4 animate-in fade-in-50">
                            {missingSkills.length > 0 ? (
                                <>
                                    <div className="flex flex-wrap gap-2">
                                        {(showAllMissing ? missingSkills : missingSkills.slice(0, 15)).map((skill) => (
                                            <Badge key={skill} variant="outline" className="text-rose-600 bg-rose-50 border-rose-100 hover:bg-rose-100 px-3 py-1.5 text-sm uppercase tracking-wide">
                                                {skill}
                                            </Badge>
                                        ))}
                                    </div>
                                    {missingSkills.length > 15 && (
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            onClick={() => setShowAllMissing(!showAllMissing)}
                                            className="text-gray-500 text-xs w-full mt-2"
                                        >
                                            {showAllMissing ? "Show Less" : `+${missingSkills.length - 15} more skills`}
                                        </Button>
                                    )}
                                </>
                            ) : (
                                <div className="flex flex-col items-center justify-center py-12 text-center text-gray-500">
                                    <CheckCircle2 className="w-12 h-12 text-emerald-500 mb-2" />
                                    <p>No missing skills found. Great job!</p>
                                </div>
                            )}
                        </TabsContent>

                        <TabsContent value="present" className="animate-in fade-in-50">
                            <div className="flex flex-wrap gap-2">
                                {presentSkills.map((skill) => (
                                    <Badge key={skill} variant="outline" className="text-emerald-700 bg-emerald-50 border-emerald-100 px-3 py-1.5 text-sm uppercase tracking-wide">
                                        {skill}
                                    </Badge>
                                ))}
                                {presentSkills.length === 0 && (
                                    <p className="text-gray-500 italic">No skills matched yet.</p>
                                )}
                            </div>
                        </TabsContent>
                    </Tabs>
                </CardContent>
            </Card>

            {/* Trajectory Simulation */}
            {trajectory && trajectory.length > 0 && (
                <Card className="border-0 shadow-lg bg-gradient-to-r from-gray-900 to-indigo-900 text-white ring-1 ring-gray-900/5">
                    <CardHeader>
                        <CardTitle className="flex items-center text-white">
                            <Sparkles className="w-5 h-5 mr-3 text-yellow-400" />
                            Job-Fit Simulation
                        </CardTitle>
                        <CardDescription className="text-gray-300">
                            Impact of learning new skills on your match score.
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {trajectory.map((item, i) => (
                                <div key={i} className="bg-white/10 backdrop-blur-md rounded-lg p-4 hover:bg-white/20 transition-all border border-white/10">
                                    <div className="flex justify-between items-start mb-2">
                                        <Badge className="bg-indigo-500 hover:bg-indigo-600 text-white border-0">
                                            + Learn {item.skill}
                                        </Badge>
                                        <span className="text-yellow-400 font-bold text-xl">
                                            +{item.boost}%
                                        </span>
                                    </div>
                                    <div className="mt-3">
                                        <div className="flex justify-between text-xs text-gray-300 mb-1">
                                            <span>Current Score</span>
                                            <span>Potential</span>
                                        </div>
                                        <div className="h-2 bg-gray-700 rounded-full overflow-hidden flex">
                                            <div
                                                className="h-full bg-gray-500"
                                                style={{ width: `${currentScore}%` }}
                                            />
                                            <div
                                                className="h-full bg-yellow-400 animate-pulse"
                                                style={{ width: `${item.boost}%` }}
                                            />
                                        </div>
                                        <div className="flex justify-between text-xs font-mono mt-1">
                                            <span>{Math.round(currentScore)}%</span>
                                            <span className="text-yellow-400">{item.new_score}%</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}
