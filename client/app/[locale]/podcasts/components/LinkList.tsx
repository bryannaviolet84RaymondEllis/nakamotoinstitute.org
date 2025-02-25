import Link from "next/link";

type Link = {
  href: string;
  label: string;
};

type LinkListProps = {
  title: string;
  links: (Link | false)[];
};

export function LinkList({ title, links }: LinkListProps) {
  return (
    <div className="flex items-baseline gap-2">
      <h2 className="font-bold">{title}:</h2>
      <ul className="flex items-center">
        {links
          .filter((link): link is Link => Boolean(link))
          .map((link, i) => (
            <li
              key={i}
              className="before:text-taupe before:mx-2 before:content-['•'] first:before:mx-0 first:before:content-none"
            >
              <Link href={link.href} className="underline">
                {link.label}
              </Link>
            </li>
          ))}
      </ul>
    </div>
  );
}
