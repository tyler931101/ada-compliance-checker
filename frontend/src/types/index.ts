export interface Violation {
    ruleId: string;
    message: string;
    element: string;
    selector: string;
    codeSnippet: string;
}
  
export interface CheckResult {
    violations: Violation[];
}