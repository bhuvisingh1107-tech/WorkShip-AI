type PageContainerProps = {
  title: string;
};

export function PageContainer({ title }: PageContainerProps) {
  return (
    <section className="px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
      <h1 className="text-2xl font-semibold tracking-tight text-slate-950">
        {title}
      </h1>
      <p className="mt-2 text-sm text-slate-500">Coming Soon</p>
    </section>
  );
}
