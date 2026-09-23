export function Rtfm({ line }: { line: string }) {
  return (
    <p className="border-l-2 border-gold pl-3 text-sm text-fg/90">
      <span className="num mr-2 text-xs tracking-[0.16em] text-gold uppercase">RTFM</span>
      {line}
    </p>
  );
}
