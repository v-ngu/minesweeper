import ReactSelect, { GroupBase, Props, SingleValue } from "react-select";

export type StringValueOption = SingleValue<{ value: string; label: string }>;

export function Select<
  Option,
  IsMulti extends boolean = false,
  Group extends GroupBase<Option> = GroupBase<Option>
>(props: Props<Option, IsMulti, Group>) {
  return (
    <ReactSelect
      {...props}
      menuPortalTarget={document.body}
      placeholder="Select difficulty"
      styles={{
        control: (base) => ({
          ...base,
          backgroundColor: `var(--dark)`,
          borderRadius: `var(--borderRadius)`,
          borderColor: `var(--dark)`,
          padding: `calc(var(--baseUnit) * 0.5)`,
          width: "calc(var(--baseUnit) * 24)",
          ":hover": {
            ...base[":hover"],
            border: "1px solid var(--accentSecondary)",
          },
        }),
        dropdownIndicator: (base, state) => ({
          ...base,
          color: state.isFocused ? `var(--accent)` : base.color,
          ":hover": {
            color: `var(--accent)`,
          },
        }),
        menu: (base) => ({
          ...base,
          backgroundColor: `var(--darkTertiary)`,
          borderRadius: `var(--borderRadius)`,
          borderColor: `var(--secondary)`,
        }),
        menuPortal: (base) => ({ ...base, zIndex: 9999 }),
        option: (base, { isDisabled, isFocused }) => ({
          ...base,
          color: isFocused ? `var(--accentSecondary)` : `var(--primary)`,
          borderRadius: `var(--borderRadius)`,
          backgroundColor: isDisabled
            ? undefined
            : isFocused
            ? `var(--darkQuaternary)`
            : undefined,
          ":hover": {
            color: `var(--accentSecondary)`,
          },
        }),
        singleValue: (base) => ({
          ...base,
          color: `var(--primary)`,
        }),
      }}
    />
  );
}
